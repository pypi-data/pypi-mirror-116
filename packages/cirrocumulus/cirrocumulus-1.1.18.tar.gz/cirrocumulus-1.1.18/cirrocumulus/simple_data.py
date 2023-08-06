import numpy as np
import pandas as pd
import scipy.sparse

from cirrocumulus.io_util import cirro_id


def get_scanpy_marker_keys(dataset):
    scanpy_marker_keys = []
    for key in dataset.uns.keys():
        rank_genes_groups = dataset.uns[key]
        if isinstance(rank_genes_groups, dict) and 'names' in rank_genes_groups and (
                'pvals' in rank_genes_groups or 'pvals_adj' in rank_genes_groups or 'scores' in rank_genes_groups):
            scanpy_marker_keys.append(key)
    return scanpy_marker_keys


def get_pegasus_marker_keys(dataset):
    marker_keys = []
    for key in dataset.varm.keys():
        d = dataset.varm[key]
        if isinstance(d, np.recarray):
            try:
                ''.join(d.dtype.names).index('log2Mean')
                marker_keys.append(key)
            except ValueError:
                pass
    return marker_keys


class SimpleData:

    def __init__(self, X, obs, var):
        self.obs = obs
        self.var = var
        self.uns = {}
        if X is not None:
            if len(X.shape) == 1:
                X = np.array([X]).T
            n_var = X.shape[1]
            n_obs = X.shape[0]
        else:
            n_var = len(var) if var is not None else 0
            n_obs = len(obs) if obs is not None else 0
        self.X = X
        self.shape = (n_obs, n_var)

    @staticmethod
    def view(adata, row_slice):
        X = adata.X[row_slice] if adata.X is not None else None
        obs = adata.obs[row_slice] if adata.obs is not None else None
        return SimpleData(X, obs, adata.var)

    @staticmethod
    def obs_stats(df, columns):
        df = df[columns]
        # variables on columns, stats on rows, transpose so that stats are on columns
        return df.agg(['min', 'max', 'sum', 'mean']).T

    @staticmethod
    def X_stats(df, var_ids):
        df = df[var_ids]
        if len(df) == 0:
            zeros = np.full(len(var_ids), 0)
            empty = np.full(len(var_ids), np.nan)
            return pd.DataFrame(
                data={'min': empty, 'max': empty, 'sum': zeros,
                      'numExpressed': zeros,
                      'mean': empty}, index=var_ids)

        return pd.DataFrame(
            data={'min': np.min(df.values, axis=0), 'max': np.max(df.values, axis=0), 'sum': df.sum().values,
                  'numExpressed': (df.values != 0).sum(axis=0),
                  'mean': df.mean().values}, index=var_ids)

    @staticmethod
    def get_var_indices(adata, names):
        return adata.var.index.get_indexer_for(names)

    @staticmethod
    def find_markers(adata, key, n_genes):
        import scipy.stats as ss
        import logging
        logger = logging.getLogger("cirro")

        marker_results = []  # array of category, name, id, features
        category = key

        for cat in adata.obs[key].cat.categories:
            logger.info('Computing markers for {}, {}'.format(key, cat))
            mask = adata.obs[key] == cat
            ds1 = adata[mask]
            ds_rest = adata[~mask]
            gene_names_keep = ds1.X.mean(axis=0) > ds_rest.X.mean(axis=0)
            if isinstance(gene_names_keep, np.matrix):
                gene_names_keep = gene_names_keep.A1
            if len(gene_names_keep) == 0:
                continue
            ds1 = ds1[:, gene_names_keep]
            ds_rest = ds_rest[:, gene_names_keep]
            pvals = np.full(ds1.shape[1], 1.0)
            ds1_X = ds1.X
            ds_rest_X = ds_rest.X
            is_sparse = scipy.sparse.isspmatrix(ds1_X)
            for i in range(ds1.shape[1]):
                v1 = ds1_X[:, i]
                v2 = ds_rest_X[:, i]
                if is_sparse:
                    v1 = v1.toarray()[:, 0]
                    v2 = v2.toarray()[:, 0]
                try:
                    _, pvals[i] = ss.mannwhitneyu(v1, v2, alternative="two-sided")
                except ValueError:
                    # All numbers are identical
                    pass
            fc = ds1_X.mean(axis=0) - ds_rest_X.mean(axis=0)
            if isinstance(fc, np.matrix):
                fc = fc.A1
            df = pd.DataFrame(data=dict(pvals=pvals, fc=fc), index=ds1.var_names)
            df = df.sort_values(by=['pvals', 'fc'], ascending=[True, False])
            features = df[:n_genes].index.values
            marker_results.append(dict(category=category, name=str(cat), features=features))
        return marker_results

    @staticmethod
    def schema(datasets):
        """ Gets dataset schema.

        Returns
            schema dict. Example:
            {"version":"1.0.0",
            "categoryOrder":{
                "louvain":["0","1","2","3","4","5","6","7"],
                "leiden":["0","1","2","3","4","5","6","7"]},
            "var":["TNFRSF4","CPSF3L","ATAD3C"],
            "obs":["percent_mito","n_counts"],
            "obsCat":["louvain","leiden"],
            "shape":[2638,1838],
            "embeddings":[{"name":"X_pca","dimensions":3},{"name":"X_pca","dimensions":2},{"name":"X_umap","dimensions":2}]
        }
        """
        obs_cat = []
        obs = []

        marker_results = []
        de_results_format = 'records'
        for dataset in datasets:
            prior_marker_results = dataset.uns.get('markers', [])

            if isinstance(prior_marker_results, str):
                import json
                prior_marker_results = json.loads(prior_marker_results)
        marker_results += prior_marker_results

        n_genes = 10
        de_results = []  # array of dicts containing params logfoldchanges, pvals_adj, scores, names
        category_to_order = {}
        embeddings = []
        field_to_value_to_color = dict()  # field -> value -> color
        for i in range(len(datasets)):
            dataset = datasets[i]
            for scanpy_marker_key in get_scanpy_marker_keys(dataset):
                rank_genes_groups = dataset.uns[scanpy_marker_key]
                params = rank_genes_groups['params']
                prefix = None if i == 0 else dataset.uns.get('name')

                # pts and pts_rest in later scanpy versions

                rank_genes_groups_keys = list(rank_genes_groups.keys())
                for k in ['params', 'names']:
                    if k in rank_genes_groups_keys:
                        rank_genes_groups_keys.remove(k)
                if 'pvals' in rank_genes_groups_keys and 'pvals_adj' in rank_genes_groups_keys:
                    rank_genes_groups_keys.remove('pvals')
                category = '{} ({})'.format(params['groupby'], scanpy_marker_key)
                de_result_name = category if prefix is None else prefix + '-' + category
                de_result_df = None
                group_names = rank_genes_groups['names'].dtype.names
                for group_name in group_names:
                    group_df = pd.DataFrame(index=rank_genes_groups['names'][group_name])

                    for rank_genes_groups_key in rank_genes_groups_keys:
                        values = rank_genes_groups[rank_genes_groups_key][group_name]
                        column_name = '{}:{}'.format(group_name, rank_genes_groups_key)
                        group_df[column_name] = values
                    group_df = group_df[group_df.index != 'nan']
                    if de_result_df is None:
                        de_result_df = group_df
                    else:
                        de_result_df = de_result_df.join(group_df, how='outer')
                    if n_genes > 0:
                        marker_results.append(
                            dict(category=de_result_name, name=str(group_name), features=group_df.index[:n_genes]))

                if de_results_format == 'records':
                    de_result_data = de_result_df.reset_index().to_dict(orient='records')
                else:
                    de_result_data = dict(index=de_result_df.index)
                    for c in de_result_df:
                        de_result_data[c] = de_result_df[c]

                de_result = dict(id=cirro_id(),
                                 color='logfoldchanges' if 'logfoldchanges' in rank_genes_groups_keys else
                                 rank_genes_groups_keys[0],
                                 size='pvals_adj' if 'pvals_adj' in rank_genes_groups_keys else rank_genes_groups_keys[
                                     0],
                                 params=params, groups=group_names, fields=rank_genes_groups_keys, type='de',
                                 name=de_result_name)
                de_result['data'] = de_result_data
                de_results.append(de_result)
            for varm_field in get_pegasus_marker_keys(dataset):
                de_res = dataset.varm[varm_field]
                names = de_res.dtype.names
                field_names = set()  # e.g. 1:auroc
                group_names = set()
                for name in names:
                    index = name.index(':')
                    field_name = name[index + 1:]
                    group_name = name[:index]
                    field_names.add(field_name)
                    group_names.add(group_name)
                group_names = list(group_names)
                field_names = list(field_names)

                de_result_df = pd.DataFrame(data=de_res, index=dataset.var.index)
                de_result_df.index.name = 'index'
                if de_results_format == 'records':
                    de_result_data = de_result_df.reset_index().to_dict(orient='records')
                else:
                    de_result_data = dict(index=de_result_df.index)
                    for c in de_res:
                        de_result_data[c] = de_result_df[c]

                de_result = dict(id=cirro_id(), type='de', name='pegasus_de',
                                 color='log2FC' if 'log2FC' in field_names else field_names[0],
                                 size='mwu_qval' if 'mwu_qval' in field_names else field_names[0],
                                 groups=group_names,
                                 fields=field_names)
                de_result['data'] = de_result_data
                de_results.append(de_result)

                if n_genes > 0:
                    field_use = None
                    for field in ['mwu_qval', 'auroc', 't_qval']:
                        if field in field_names:
                            field_use = field
                            break
                    if field_use is not None:
                        field_ascending = field_use != 'auroc'
                        for group_name in group_names:
                            fc_column = '{}:log2FC'.format(group_name)
                            name = '{}:{}'.format(group_name, field_name)
                            idx_up = de_result_df[fc_column] > 0
                            df_up = de_result_df.loc[idx_up].sort_values(by=[name, fc_column],
                                                                         ascending=[field_ascending, False])
                            features = df_up[:n_genes].index.values
                            marker_results.append(dict(category='markers', name=str(group_name), features=features))

            for key in dataset.obs_keys():
                if pd.api.types.is_categorical_dtype(dataset.obs[key]) or pd.api.types.is_bool_dtype(
                        dataset.obs[key]) or pd.api.types.is_object_dtype(dataset.obs[key]):
                    obs_cat.append(key)
                else:
                    obs.append(key)

            # if 'metagenes' in dataset.uns:
            #     metagenes = dataset.uns['metagenes']
            #     schema_dict['metafeatures'] = metagenes['var'].index

            for key in dataset.obs_keys():
                if pd.api.types.is_categorical_dtype(dataset.obs[key]) and len(dataset.obs[key]) < 1000:
                    category_to_order[key] = dataset.obs[key].cat.categories

            # spatial_node = adata.uns['spatial'] if 'spatial' in adata.uns else None
            #
            # if spatial_node is not None:
            #     spatial_node_keys = list(spatial_node.keys())  # list of datasets
            #     if len(spatial_node_keys) == 1:
            #         spatial_node = spatial_node[spatial_node_keys[0]]

            images_node = dataset.uns.get('images',
                                          [])  # list of {type:image or meta_image, name:image name, image:path to image, spot_diameter:Number}
            image_names = list(map(lambda x: x['name'], images_node))

            for key in dataset.obsm_keys():
                dim = dataset.obsm[key].shape[1]
                if 1 < dim <= 3:
                    embedding = dict(name=key, dimensions=dim)
                    if dim == 2:
                        try:
                            image_index = image_names.index(key)
                            embedding['spatial'] = images_node[image_index]
                        except ValueError:
                            pass

                    embeddings.append(embedding)
            meta_images = dataset.uns.get('meta_images', [])
            for meta_image in meta_images:
                embeddings.append(meta_image)

            for key in dataset.uns.keys():
                if key.endswith('_colors'):
                    field = key[0:len(key) - len('_colors')]
                    if field in dataset.obs:
                        colors = dataset.uns[key]
                        if pd.api.types.is_categorical_dtype(dataset.obs[field]):
                            categories = dataset.obs[field].cat.categories
                            if len(categories) == len(colors):
                                color_map = dict()
                                for i in range(len(categories)):
                                    color_map[str(categories[i])] = colors[i]
                                field_to_value_to_color[field] = color_map
                        else:
                            print("Skipping colors for {}".format(key))
        schema_dict = {'version': '1.0.0'}
        schema_dict['results'] = de_results
        schema_dict['colors'] = field_to_value_to_color
        schema_dict['markers'] = marker_results
        schema_dict['embeddings'] = embeddings
        schema_dict['categoryOrder'] = category_to_order
        var_ids = []
        for dataset in datasets:
            var_ids += dataset.var.index.to_list()
        schema_dict['var'] = var_ids
        schema_dict['obs'] = obs
        schema_dict['obsCat'] = obs_cat
        nfeatures = 0
        for dataset in datasets:
            nfeatures += dataset.shape[1]
        schema_dict['shape'] = [datasets[0].shape[0], nfeatures]
        return schema_dict

    @staticmethod
    def to_df(adata, obs_measures, var_measures, dimensions, basis=None):
        df = pd.DataFrame()
        obs_keys = obs_measures + dimensions
        if basis is not None:
            obs_keys += basis['coordinate_columns']

        for key in obs_keys:
            df[key] = adata.obs[key]
        indices = SimpleData.get_var_indices(adata, var_measures)
        for i in range(len(var_measures)):
            X = adata.X[:, indices[i]]
            if scipy.sparse.issparse(X):
                X = X.toarray()
            df[var_measures[i]] = X
        return df
