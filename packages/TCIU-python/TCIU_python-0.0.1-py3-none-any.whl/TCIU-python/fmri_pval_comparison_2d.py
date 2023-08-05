import sys
from matplotlib.pyplot import legend, text
import numpy as np
from numpy.lib.arraysetops import isin
from plotnine.geoms import geom_text
from fmri_2dvisual import fmri_2dvisual
import pandas as pd
import seaborn as sns
def islist(array):
    if(not isinstance(array,list) and not isinstance(array,np.ndarray)):
        return False
    else:
        return True
def fmri_pval_comparison_2d(pval_ls,pval_name_ls,axis_i_lses,hemody_data=None,mask=None,p_threshold=0.05,legend_show=True,method="scale_p",color_pal="Yl0Rd",multi_pranges=True,mask_width=1.5):

        if( not all(len(x)==3 for x in axis_i_lses) ):
            print("Every axis_i_ls element must have length 3 for each of the coordinates")
            sys.exit()
        

        if(method not in ["scale_p","min_max"]):
            print("method should only choose from scale p and min_max.")
            sys.exit()
        if(not isinstance(legend_show,bool)):
            print("legend_show must be a boolean variable")
            sys.exit()
        if(not isinstance(p_threshold,float)):
            print("p_threshold must me a numerical value. Please enter a floating point between 0 and 1")

            sys.exit()
        if(not isinstance(mask,np.ndarray) and not isinstance(mask,list) and len(mask.shape)!=3):
            print("mask should be a 3D list or an array")    
            sys.exit()
        if(not isinstance(hemody_data,list) and not isinstance(hemody_data,np.ndarray) and len(hemody_data.shape)!=3):
            print("hemody_data must be a 3d array")
            sys.exit()
        if(not isinstance(pval_ls,list) and not isinstance(pval_ls,np.ndarray) and len(pval_ls)!=len(pval_name_ls) and not isinstance(pval_name_ls,list) and isinstance(pval_name_ls,np.ndarray)):
            print("p_val_ls and pval_name_ls should be a list or array with equal lengths.")    
            sys.exit()
        if(islist(axis_i_lses) and islist(axis_i_lses[0])):
            axis_i_ls=np.array(axis_i_lses)
            #2d array
            axis_i_ls=axis_i_ls.flatten()
            if(len(axis_i_ls)!=3*len(axis_i_lses)):
                print(" If axis_i_ls contains more than one list of index each list must have 3 elements for x,y,z")
        elif(not islist(axis_i_lses) and isinstance(axis_i_lses[0],float) and len(axis_i_lses)==3):
            axis_i_ls=np.array(axis_i_lses)
            axis_i_ls=np.tile(axis_i_ls,len(pval_ls))
        elif(not isinstance(axis_i_lses,list) and not isinstance(axis_i_lses,np.ndarray) or len(axis_i_lses)!=3):
            print("axis_i_ls should be list with 3 elements x,y,z")




        len_idx_sets=(len(axis_i_ls)/3)
        axis_vec=np.tile(["x","y","z"],len_idx_sets)
        axis_i_vec=axis_i_ls.flatten()       



        pl_name_vec={}
        ing_pls_name_vec=[]
        idx=0
        p1=None
        for i in range(len(pval_ls)):
            for axis_ele in axis_vec:
                idx=idx+1
                try:
                    p1=fmri_2dvisual(pval_ls[i],axis_ls=axis_ele,mask=mask,p_threshold=p_threshold,legend_show=legend_show,method=method,color_pal=color_pal,multi_pranges=multi_pranges,mask_width=mask_width,hemody_data=hemody_data)
                
                except Exception as ex:
                    print("the mistake is at the 3d plot function")
                    print("the message error in 2d plot is ",ex)
                    print("The wrong plot is ",axis_ele+str(i))
                    print("The number represents the plot for which p values in x,y,and z represents the sagittal, coronal, and axial view")
                    
                    sys.exit()
                    
                p1_name=axis_ele+str(i)
                pl_name_vec[p1_name]=p1
            ing_pls_name_vec.append("pls"+str(i))
        plt_items={}
        for plt_item in ing_pls_name_vec:
            
            start_idx=idx*len(axis_vec)+1
            end_idx=(idx+1)*len(axis_vec)
            int_plt_str=list(pl_name_vec.items())[start_idx:end_idx]
            idx=idx+1
            text_str=pval_name_ls[idx]
            int_plt_str_trueval=[int]
            int_plts_form=int_plt_str_trueval.append({"nrow":1,"ncol":1+len(axis_vec)})
            int_plt=geom_text(text_str)
            plt_items[plt_item]=int_plt
        if(legend_show==False):
            complement_p_cut=[]
            one_minus_p_range=

            label_p_range=[]
        for i in range(len(numeri_range_one_minus_p)):
            p_2range=1-int(numeric_range_one_minus_p[i])
            label_p_range[i]="({},{}]".format(p_2range[1],p_2range[0])
        p_range_num=pd.Series(label_p_range)
        p_range_num=prange_num.astype("category")
        p_range_num=p_range_num.sort_values()
        p_range_num=p_range_num.astype("int64")
        one_minus_p_color=sns.color_palette("YlOrRd",9)[p_range_num]

        p_range_num_df=pd.DataFrame({"x":p_range_num,"y":p_range_num,"color_i":one_minus_p_color})
        color_i=one_minus_p_color
        p=ggplot()+geom_title(mapping=aes(x=p_range_num_df["x"],y=p_range_num_df["y"],fill=p_range_num_df["color_i"]))
        +scale_fill_manual(value=label_p_range,breaks=np.flip(np.sort(np.unique(p_range_num_df["color_i"])))+theme(legend_position="bottom")

        ing_pls_name_trueval=
        ing_pls_name_form=legend_p.extend(ing_pls_name_trueval)
        fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(7, 7))

        else:
            ing_pls_name_trueval=apply(ing_pls_name_vec,get)
            fig,axes=plt.subplot(nrows=3,ncols=2,figsize=(7,7))