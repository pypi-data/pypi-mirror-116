from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
from plotly.graph_objects import Layout
def time(array):
    return [x+1 for x in range(len(array))]
def GTSplot(tsdata,newtitle="result",ylab="value",xlab="time",unit=None,ts_name=None,title_size=10,colo=None):
    fig = go.Figure()

    for i in range(tsdata.shape[1]):
        tsd=tsdata[:,i-1]
        tsn=ts_name[i-1]
        col=colo[i-1]
        tsp=fig.add_trace(go.Scatter(x=[x+1 for x in range(len(tsd))],
         y=tsd,text=" ".join([x+1 for x in range(len(tsd))]),
                    mode='lines',
                    name=tsn,opacity=0.75,name=tsn))
    layout=Layout(title=dict(text=newtitle,font=dict(family="Times New Roman",size=title_size,color="black")),paper_bgcolor="rgb(255,255,255)",plot_bgcolor="rgb(229,229,229)",xaxis=dict(title=xlab,gridcolor="rgb(255,255,255)",showgrid=True,showline=False,showticklabels=True,tickcolor="rgb(127,127,127)",ticks="outside",zeroline=False),yaxis=dict(title=ylab
    ,gridcolor="rgb(255,255,255)",showgrid=True,showline=False,showticklabels="rgb(127,127,127)",ticks="outside",zeroline=False))
    fig.update_layout(layout)
    return fig

def TSplot_gen(origin_t,ARIMAmodel,XREG=None,periods=None,NEWtitle="Result",Ylab="Value",Xlab="time",plot_labels=None,ts_original="original time series",ts_forecast="forecasted time series",title_size=10,ts_list="empty",ts_labels=None,ts_names=None,COLO=None):
    tsmodel=[]

    if (origin_t=="all"):
        TIME=1
    else:
        TIME=len(tsmodel["x"])-origin_t+1
    includetime=[tsmodel["x"][TIME:len(tsmodel["x"])]].extend([None]*len(tsmodel["mean"]))
    includetime2=[None]*len(time(tsmodel["x"])[TIME:len(tsmodel["x"])])
    includetime2.extend(tsmodel["mean"])
    includetime3=[None]*len(time(tsmodel["x"])[TIME:len(tsmodel["x"])])
    includetime3.extend(tsmodel["lower"][0])
    includetime4=[None]*len(time(tsmodel["x"])[TIME:len(tsmodel["x"])])
    includetime4.extend(tsmodel["upper"][0])
    includetime5=[None]*len(time(tsmodel["x"])[TIME:len(tsmodel["x"])])
    includetime5.extend(tsmodel["lower"][1])
    includetime6=[None]*len(time(tsmodel["x"])[TIME:len(tsmodel["x"])])
    includetime6.extend(tsmodel["upper"][1])
    alltime=time(tsmodel["x"])[TIME:len(tsmodel["x"])]
    alltime.extend(time(tsmodel["mean"]))
    tsp=go.Figure()
    tsp.add_trace(go.Scatter(mode="lines"))
    layout=Layout(title=dict(text=NEWtitle,font=dict(family="Times New Roman",size=title_size,color="black")),paper_bgcolor="rgb(255,255,255)",plot_bgcolor="rgb(229,229,229)",xaxis=dict(title=Xlab,gridcolor="rgb(255,255,255)",showgrid=True,showline=False,showticklabels=True,tickcolor="rgb(127,127,127)",ticks="outside",zeroline=False),yaxis=dict(title=Ylab
    ,gridcolor="rgb(255,255,255)",showgrid=True,showline=False,showticklabels="rgb(127,127,127)",ticks="outside",zeroline=False))
    tsp.add_trace(go.Scatter(type="line",x=alltime,text=plot_labels,y=includetime,name=ts_original,line=dict(color="powderblue"),fill="tonexty",fillcolor="powderblue",name="95 per upper bound"))
    tsp.add_trace(go.Scatter(type="line",x=alltime,text=plot_labels,y=includetime2,name=ts_original,line=dict(color="red"),fill="tonexty",fillcolor="powderblue",name=ts_forecast))
    tsp.add_trace(go.Scatter(type="line",x=alltime,text=plot_labels,y=includetime3,name=ts_original,line=dict(color="powderblue"),fill="tonexty",fillcolor="powderblue",name="80 per lower bound"))
    tsp.add_trace(go.Scatter(type="line",x=alltime,text=plot_labels,y=includetime4,name=ts_original,line=dict(color="powderblue"),fill="tonexty",fillcolor="lightpink",name="80 per upper bound"))
    tsp.add_trace(go.Scatter(type="line",x=alltime,text=plot_labels,y=includetime5,name=ts_original,line=dict(color="powderblue"),fill="tonexty",fillcolor="powderblue",name="95 per lower bound"))
    tsp.add_trace(go.Scatter(type="line",x=alltime,text=plot_labels,y=includetime6,name=ts_original,line=dict(color="powderblue"),fill="tonexty",fillcolor="powderblue",name="95 per upper bound"))


def fmri_split_ab_bl(vect, option="vector"):
    if(option=="list"):
        overallen=len(np.where(vect!=0))
        ab_len=len(np.where(vect>0))
        b1_len=len(np.where(vect<0))
        null_list=[x for x in range(overallen)]
        s=["#FFFF00", "#FFFF41", "#FFFF60" ,"#FFFF7A" ,"#FFFF92" ,"#FFFFA9" ,"#FFFFBF","#FFFFD4" ,"#FFFFEA" ,"#FFFFFF"]
        for i in range(b1_len):
            null_list[i]=[(i-1)/overallen,s[i]]
        s=[ "#FFFFFF", "#F0E5FF", "#E0CBFF", "#CFB1FF", "#BD98FF" ,"#A87FFF" ,"#9265FF","#774BFF" ,"#542EFF" ,"#0000FF"]
        for i in range(ab_len):
            null_list[b1_len-1+i]=[(b1_len-1+i-1)/overallen,s[i]]

    elif(option=="vector"):
        overallen=len(np.where(vect!=0))
        ab_len=len(np.where(vect>0))
        b1_len=len(np.where(vect<0))
        null_list=np.array([None]*overallen)
        s=["#FFFF00", "#FFFF41", "#FFFF60" ,"#FFFF7A" ,"#FFFF92" ,"#FFFFA9" ,"#FFFFBF","#FFFFD4" ,"#FFFFEA" ,"#FFFFFF"]
        for i in range(b1_len):
            null_list[i]=s[i]
        s=[ "#FFFFFF", "#F0E5FF", "#E0CBFF", "#CFB1FF", "#BD98FF" ,"#A87FFF" ,"#9265FF","#774BFF" ,"#542EFF" ,"#0000FF"]
        for i in range(ab_len):
            null_list[b1_len-2+i]=s[i-1]

    return null_list