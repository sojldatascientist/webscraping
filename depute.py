
from random import randint
from time import time 
import pandas as pd
import unicodedata,os
from PIL import Image
from resizeimage import resizeimage

import streamlit as st

import plotly.express as px

import csv
import numpy as np



import sys
import altair as alt
import urllib






if sys.version_info[0] < 3:
    reload(sys) 
    sys.setdefaultencoding("utf-8")
                                  ############## ENTETE ###############
# chargement des donnees

df =  st.cache(pd.read_csv)("declarationD.csv",index_col ="Unnamed: 0" )
df = df.iloc[:-1,:]
comp = df.T.describe()
d = df.T
#df1 = df
d["annee"] = d.index
region = st.cache(pd.read_csv)("dep_region.csv",index_col = "Unnamed: 0")





            ####### affichage de la photo du deputes choisis

#from PIL import Image

os.chdir("assets")
           # Entrer dans le repertoire qui contient les fichiers
x = os.listdir()
p =  [int(j.split(".")[1]) for j in [i for i in x if i.endswith("jpg")] ] 

os.chdir("../")

##################### ANALYSE COMPARATIVE ou ANALYSE SINGULIERE ########################################
# ajout du logo de EDC 
class   Application :

  def __init__(self):

      self.menus = Menu()

  # def afficheMessage(self):
  #     return st.markdown("""<samp>Voici ma première page.</samp>""",unsafe_allow_html=True)

class AnalyseSinguliere :
  def __init__(self):
    self.axe = list(df.columns)
    nom = st.sidebar.selectbox("", list(comp.columns)) #Nom et Prenoms
    self.nom = nom
    index_nom = list(comp.columns).index(nom)
    self.index_nom = index_nom
    self.nom_img = str(nom) +"."+ str(index_nom) + ".jpg"
    self.afficheNom(self.nom + ", {}".format(list(region.iloc[self.index_nom])[0]) )
    self.affichePhotos()
    self.afficheSalaire()
    self.axEtude()
    self.visualisationPersonalisee()
     #### Affichage de la photo
    #nom_img = str(nom) +"."+ str(index_nom) + ".jpg"


  def afficheNom(self,nom):
    html_temp = """<center><h1 style="background-color:black;color:white;font-size:30px">{}</h1></center> <br>""".format(nom)
    return st.markdown(html_temp,unsafe_allow_html=True)

  def affichePhotos(self):
    try: 
          image = Image.open('assets/photos/{}'.format(self.nom_img))

    except :
         image = Image.open('assets/vide.png').convert('RGB')
    return st.sidebar.image(image,width=None,caption='{}'.format(list(region.iloc[self.index_nom])[0]),use_column_width=True)
  
  def afficheSalaire(self):
               ################ Affichage de toutes les informations du depute selectionnee
      dataf = st.sidebar.radio("Salaire ",("fiche des parlementaires","fiche personnalisee"))
      annee = list(df.columns)
      if dataf == "fiche des parlementaires":
            return st.write(df)
      elif dataf == "fiche personnalisee" :
        return st.write(df.iloc[self.index_nom,:] ) # mettre la visu cote a cote





  def axEtude(self):

      # axe de visualisation
    st.markdown("**Resume**")
    axes = st.sidebar.multiselect("Choisir des axes d'analyse",df.columns)
    axes = sorted(axes)
    self.axe = axes

    if len(self.axe) != 0 :  # si l'on choisit au moin une colonne
         df1 = df[self.axe]
         st.markdown("Sur les annees {}".format(self.axe))

    else :
         self.axe = list(df.columns)
         df1 = df[self.axe]
    an = str(sorted(self.axe))
    pr_an = an[1:-1]

    col = ['min','moyenne','max','sum','etendu']
    montant = [df1.T.min()[self.nom],df1.T.mean()[self.nom],\
    df1.T.max()[self.nom],df1.T.sum()[self.nom],df1.T.max()[self.nom] - df1.T.min()[self.nom]]
    dict = {col[i]: montant[i] for i in range(len(col)) }
    dict["Nom et Prenoms"] =  self.nom

    return st.write(pd.DataFrame(dict, index = range(1)))

  def visualisationPersonalisee(self) :
    st.markdown("Visualisation")
    operation = st.selectbox(" ",("Line","area_Line","Bar_chart","Camember","Bulle"))
    if operation == "Histogramme" :
        fig = px.histogram(d.loc[self.axe],x=d.loc[self.axe]["annee"],y= self.nom,histfunc="sum")
        st.plotly_chart(fig)
    elif operation == "Line" :
     st.line_chart(df[self.axe].iloc[self.index_nom,:])
    elif operation == "area_Line" :
       st.area_chart(df[self.axe].iloc[self.index_nom,:])
    elif operation == "Bar_chart":
      st.bar_chart(df[self.axe].iloc[self.index_nom,:])

    elif operation == "Camember":
           #axe = st.multiselect(" abscisse & ordonnee",df1.columns)
       fig = px.pie(d.loc[self.axe],names=self.nom,title="Déclaration de {}".format(self.nom) ,
             height = 400,color=d.loc[self.axe]["annee"],
        hover_name = d.loc[self.axe]["annee"],labels = d.loc[self.axe]["annee"])
       st.plotly_chart(fig)

    elif operation == "Bulle":

      fig = px.scatter(d.loc[self.axe], x=d.loc[self.axe]["annee"] , y=d.loc[self.axe][self.nom],
           size=d.loc[self.axe][self.nom], color=d.loc[self.axe]["annee"],
                 hover_name=d.loc[self.axe]["annee"], log_x=True, size_max=60)
      return  st.plotly_chart(fig)



class Home :

  def __init__(self):
    self.titreProjet()
    self.icon()
    self.textAcceuil()

  def titreProjet(self) :
    #tomato
    html_temp = """
    <link rel="stylesheet" type="text/css" href="style.css">
      <link rel="stylesheet" type="text/css" href="css\\bootstrap.css">
      <link rel="stylesheet" type="text/css" href="css\\bootstrap.min.css">
    <center><h1 style="background-color:yellow;color:blue;font-size:30px">DONNEES STATISTIQUES
    DES DECLARATIONS FINANCIERES DE LA HAUTE AUTORITE DE FRANCE</h1></center>"""
    return st.markdown(html_temp,unsafe_allow_html=True)

# les différents liens du menu
  # def bootstrap(self):

  #   html_temp = """
  #   <link rel="stylesheet" type="text/css" href="style.css">
  #     <link rel="stylesheet" type="text/css" href="css\\bootstrap.css">
  #     <link rel="stylesheet" type="text/css" href="css\\bootstrap.min.css">"""
  #   return st.sidebar.markdown(html_temp,unsafe_allow_html=True)

  # def menu(self):
  #   html_temp = """<nav class="navbar navbar-inverse">
  #           <div class="container-fluid">
  #                 <ul class="nav navbar-nav">
  #                       <li> <a href="#">Accueil</a> </li>
  #                       <li> <a href="#">Analyse Singulière</a> </li>
  #                       <li> <a href="#">Analyse Comparative</a> </li>
  #                       <li> <a href="#">Analyse Cartographique</a> </li>
  #                 </ul>
  #                 <form class="navbar-form navbar-right inline-form">
  #                          <div class="form-group">
  #                                     <input type="search" class="input-sm form-control" placeholder="Recherche">
  #                                     <button type="submit" class="btn btn-primary btn-sm"><span class="glyphicon glyphicon-eye-open"></span> Chercher</button>
  #                          </div>
  #                 </form>
  #           </div>
  #       </nav>"""

  #   return st.sidebar.markdown(html_temp,unsafe_allow_html=True)


              ########## Affiche Logo ################

  def icon(self):
    html_temp = """<nav class="navbar navbar-light">
                       <a class="navbar-brand">
                           <div><img src="{0}" width="30" height="30" >
                                        EDC</div>
                       </a>
                   </nav>""" #.format(Image.open('bootstrap-solid.PNG'))

    image = Image.open('assets/photos/{}'.format('iicon.jpeg'))
    return st.sidebar.image(image,width=None,caption='EDC',use_column_width=True)

    #return st.sidebar.markdown(html_temp,unsafe_allow_html=True)

  def textAcceuil(self) :
      html_temp = """
      <br>
      <samp><samp style="color:black;">C</samp>onnaitre les déclarations financières des personnalités de la haute autorité
      de France, est l'objectif que nous nous sommes fixés.
      <br>
      <br>
      Scrapper et  collecter les données des déclarations financières des députés pour des travaux statistiques à partir du site
<a target = " _blank" href = https://www.hatvp.fr/ > de la haute autorité </a> le 31 janvier 2020.
Cette étude nous aidera à faire des analyses individuelles.
      <br>
      <samp><samp style="color:blue;">L'analyse individuelle</samp> établira un tableau récapitulatif des déclarations faites
      pour une et une seule personnalité. Cela s'expliquera par de diverses visualisations graphiques
      sur des axes définis."""
      return st.markdown(html_temp,unsafe_allow_html=True)



### Analyse comparative
class Compare :
  """Top 5, fort et less"""

  def __init__(self):
    self.comp = comp
    self.dic=None
    self.operation = None
    self.test()
    st.write(self.dic[self.operation])
    st.write(self.comp)

  def test(self):
    st.markdown("Test sur ")
    dic = {'minimum':'min','valeur':'sum','maximum':'max','écart-type':'std','moyenne':'mean',
        "1er qt":'25%' ,"2eme qt":'50%', '3eme qt':'75%' ,'TABLEAU':'sum' }
    operation = st.selectbox(" ",('TABLEAU',"moyenne","écart-type","valeur","minimum","maximum",
      "1er qt" ,"2eme qt", '3eme qt' ))
    self.dic=dic

    if len(operation ) != 0 :
      self.operation = operation

      if self.operation == 'valeur' or self.operation == 'TABLEAU' :
        pass
      else :
        self.comp = self.comp.loc[self.dic[self.operation]]#.sort_values( [self.dic[self.operation]] ,
          #ascending = True )
        return self.comp




  def test_value(self):
    test = 5

class Menu :
  def __init__(self):
    self.menu()


  def menu(self):
    html_temp = """<center><h4 style="background-color:orange;color:white;font-size:15px">Collecte des
    données <a target = " _blank" href = https://www.hatvp.fr/ > du site de la haute autorité. </a> </h4></center>"""
    st.sidebar.markdown(html_temp,unsafe_allow_html=True)
    mn = st.sidebar.radio("" ,("A propos","Déclarations"))#,"Analyse comparative","Cartographie"))

    if mn == "A propos":
      h = Home()
      #return h
    elif mn == "Déclarations" :
      ns = AnalyseSinguliere()
      #return ns
    elif mn == "Analyse comparative" :
        #st.markdown(mn)
        com = Compare()

    elif mn == "Cartographie" :
      st.markdown(mn)

Application()  
