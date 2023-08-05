
class ClusteringExperiment:

    def __init__(self,exp_id="Unnamed",data=None,regressor=None,aux_data=None):

        self.id=exp_id
        self.data=data
        self.regressor=regressor
        self.aux_data=aux_data

        self._confirm_time_coords_match()
        self.regression_correlations=None
        self.regressed_pcs=None
        self.windowed_pcs=None
        self.windowed_regressed_pcs=None
        self.windowed_field_data=None
        self.windowed_regressor=None
        self.clusters={}
        self.cluster_cubes={}
        self.cluster_correlations={}

    #Not currently very rigorous.
    #Makes sure the time axes align.
    def _confirm_time_coords_match(self):

        t_axes=[]
        if self.pcs is not None:
            t_axes.append(self.pcs.coord("time"))
        if self.regressor is not None:
            t_axes.append(self.regressor.coord("time"))
        if self.field_data is not None:
            t_axes.append(self.field_data.coord("time"))

        for t_ax in t_axes:
            assert np.all(t_ax.points==t_axes[0].points)

    #regresses self.regressor against self.pcs
    def regress_pcs(self):

        if self.regressor is None:
            raise(ValueError("No regressor attribute defined."))


        corr,regressed_pc=regress_pc(self.pcs,self.regressor.data)

        self.regression_correlations=corr
        self.regressed_pcs=regressed_pc

    #Called by combine_with, and used to stick different
    #PC sequences together.
    def _combine_attribute(self,attr,cluster_array,time_coord=None):

        array=[getattr(self,attr).data]

        for C in cluster_array:
            array.append(getattr(C,attr).data)

        #The atleast_3d here helps make sure 1D attributes
        #(like the regressor) get treated the same way as 2D attributes
        array=np.vstack(np.atleast_3d(array))
        T=array.shape[0]

        new_attr=make_cube_with_different_1st_axis(getattr(self,attr),T,t_ax=time_coord)
        #We want to get rid of length 1 dimensions, hence the squeeze here
        new_attr.data=np.squeeze(array)
        return new_attr

    #Combines the current ClusteringExperiment PCs with some others,
    #appending state sequences together.
    def combine_with(self,cluster_array,time_coord=None,new_id=None):

        New_ClusterExperiment=ClusteringExperiment(exp_id=new_id)

        for attribute in ["pcs","regressed_pcs","regressor","field_data"]:
            if getattr(self,attribute) is not None:
                combined_attribute=self._combine_attribute(attribute,cluster_array,time_coord)
                setattr(New_ClusterExperiment,attribute,combined_attribute)

        return New_ClusterExperiment

    def _window_attribute(self,attribute,width,overlap):

        data=getattr(self,attribute)

        windowed_array=[]

        T=data.shape[0]
        window_num=np.floor((T-width)/overlap).astype(int)
        windows=[slice(i*overlap,(i*overlap)+width) for i in range(window_num)]

        for window in windows:
            windowed_array.append(data[window])

        return windowed_array

    def window_data(self,width,overlap):

        for attribute in ["pcs","regressed_pcs","regressor","field_data"]:
            if getattr(self,attribute) is not None:
                windowed_attribute=self._window_attribute(attribute,width,overlap)
                setattr(self,"windowed_"+attribute,windowed_attribute)


    def cluster_pcs(self,Ks,pc_list=None):

        self.Ks=Ks

        if pc_list is None:
            pc_list=["pcs","regressed_pcs","windowed_pcs","windowed_regressed_pcs"]

        for pcs in pc_list:
            if getattr(self,pcs) is not None:
                clusters=self._cluster_attribute(pcs,Ks)
                self.clusters[pcs]=clusters

    def _cluster_attribute(self,pcs,Ks):

        data=getattr(self,pcs)
        #data will either be an iris cube or a list of cubes.
        #We try and iterate and if that fails then its a cube

        try:
            clusters=[{K:Kmeans_cluster(cube.data,K) for K in Ks} for cube in data]
        except:
            clusters={K:Kmeans_cluster(data.data,K) for K in Ks}

        return clusters

    def get_cluster_cubes(self,pc_list=None):

        if pc_list is None:
            pc_list=["pcs","regressed_pcs","windowed_pcs","windowed_regressed_pcs"]

        for pc in pc_list:

            if getattr(self,pc) is not None:

                cl_data=self.clusters[pc]
                #Assume its iterable (i.e. windowed):
                try:
                    ccs=[{K:get_cluster_cube(F,cl[K].states) for K in self.Ks} for F,cl in zip(self.windowed_field_data,cl_data)]
                #If not, then its full data:
                except:

                    ccs={K:get_cluster_cube(self.field_data,cl_data[K].states) for K in self.Ks}

                self.cluster_cubes[pc]=ccs

    def _reorder_clusters(self,pc,K,mapping,window=None):

        order=np.array([m[1] for m in mapping])

        if window is None:
            #Reorder cluster cubes
            self.cluster_cubes[pc][K]=self.cluster_cubes[pc][K][order]
            #Reorder cluster data
            self.clusters[pc][K].reorder(mapping)
        else:
            #Reorder cluster cubes
            self.cluster_cubes[pc][window][K]=self.cluster_cubes[pc][window][K][order]
            #Reorder cluster data
            self.clusters[pc][window][K].reorder(mapping)


    def correlate_clusters(self,reference_clusters,reorder_clusters=False,pc_list=None,reference_id="None"):

        if pc_list is None:
            pc_list=["pcs","regressed_pcs","windowed_pcs","windowed_regressed_pcs"]

        correlation_dict={}

        for pc in pc_list:

            cubes1=self.cluster_cubes[pc]


            #Non windowed clusters:
            if type(cubes1) is dict:

                mean_corr_dict={}
                reg_corr_dict={}
                for K in self.Ks:

                    (mean_corr,reg_corrs),mapping=correlate_clusters(reference_clusters[K],cubes1[K],and_mapping=True,mean_only=False)

                    mean_corr_dict[K]=mean_corr
                    reg_corr_dict[K]=reg_corrs

                    if reorder_clusters:
                        self._reorder_clusters(pc,K,mapping,window=None)

                correlation_dict[pc]=[mean_corr_dict,reg_corr_dict]

            #Windowed clusters
            elif type(cubes1) is list:

                mean_corr_arr=[]
                reg_corr_arr=[]

                for w,cc1 in enumerate(cubes1):

                    mean_corr_dict={}
                    reg_corr_dict={}
                    for K in self.Ks:

                        (mean_corr,reg_corrs),mapping=correlate_clusters(reference_clusters[K],cc1[K],and_mapping=True,mean_only=False)

                        mean_corr_dict[K]=mean_corr
                        reg_corr_dict[K]=reg_corrs

                        if reorder_clusters:
                            self._reorder_clusters(pc,K,mapping,window=w)

                    mean_corr_arr.append(mean_corr_dict)
                    reg_corr_arr.append(reg_corr_dict)

                correlation_dict[pc]=[mean_corr_arr,reg_corr_arr]

            else:
                raise(ValueError("cubes should be stored either as a dict or list"))

        self.cluster_correlations[reference_id]=correlation_dict

    #Just a little syntactic sugar to make data retrieval more convenient

    def get_cl_data(self,pc_data,cl_attr,K,window=None):
        if window is None:
            return getattr(self.clusters[pc_data][K],cl_attr)
        else:
            return getattr(self.clusters[pc_data][window][K],cl_attr)

    def get_cc_data(self,pc_data,K,window=None):
        if window is None:
            return self.cluster_cubes[pc_data][K]
        else:
            return self.cluster_cubes[pc_data][window][K]

    def get_correlation_data(self,exp_id,pc_data,K,window):

        if window is None:
            return self.cluster_correlations[exp_id][pc_data][K]
        else:
            return self.cluster_correlations[exp_id][pc_data][window][K]
