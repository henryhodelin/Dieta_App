import streamlit as st

import pandas as pd
import numpy as np
import os

import pdfkit as pdf

import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from matplotlib.backends.backend_pdf import PdfPages

from funciones.dietcal import  dcalculo
#from funciones.informe import plantilla, article, preheader, header, create_preheader
from funciones.informe import  create_preheader

import subprocess  # Para ejecutar programas externos
import datetime    #Trabajo con fechas y horarios

st.title('CALCULADORA DE DIETAS')

Genero = st.sidebar.radio(
     "SEXO",
     ('Masculino', 'Femenino'))

nombre = st.sidebar.text_input("Nombre ", key="NAME")
#nombre = st.session_state.NAME

#st.write(nombre)

edad = st.sidebar.number_input("Edad (Años) ")
altura = st.sidebar.number_input("Altura (cm) ")
peso = st.sidebar.number_input("Peso actual (kg)")


vpeso = st.sidebar.slider('Variación de Peso (kg) deseada en un mes', -3.0, 3.0, 0.0)
#st.write("Quiero  que mi peso varie en ", vpeso, ' kilogramos')


fecha=datetime.date.today()
FechaYHora=datetime.datetime.now()

directory = os.getcwd()

if edad > 0 and altura > 0 and peso > 0 :
    AlturaM=altura/100.0
    #st.write(AlturaM)
    IMC=peso/(AlturaM**2)
    
    Estado= ''
    Recomendacion=''
    archivo =  nombre + '-' +str(fecha) + '.tex'
    archivopdf = nombre + '-' +str(fecha) + '.pdf'
    #st.write('El nombre del archivo es ' + archivo )
    
    
    if IMC < 18.50:
        Estado = ' BAJO PESO' 
        Recomendacion=' aumentar hasta su peso ideal'
    elif IMC > 18.50 and IMC < 24.99 :
        Estado = ' NORMAL'
        Recomendacion=' mantenerse cerca su peso ideal'
    elif IMC > 24.99 and IMC < 29.99 :
        Estado = ' PRE OBESIDAD'
        Recomendacion= ' disminuir hasta su peso ideal'
    else:
        Estado = 'OBESIDAD'
        RecomendacionH= ' disminuir urgentemente hasta su peso ideal'
    
    if Genero == 'Masculino':
        BMR = (10.0*peso) + (6.25*altura) - (5.0*edad) + 5 
        PesoIdeal =22.5*(AlturaM**2)
        PorcentajeGrasa=(1.2*IMC)+(0.23*edad)-10.8-5.4
        IMCIdeal = PesoIdeal/(AlturaM**2)
        PorcentajeGrasaIdeal=(1.2*IMCIdeal)+(0.23*edad)-10.8-5.4
    elif  Genero == 'Femenino':
        IMC=peso/(AlturaM**2)
        BMR = (10.0*peso) + (6.25*altura) - (5.0*edad) - 161.0
        PesoIdeal =21.5*(AlturaM**2)
        PorcentajeGrasa=(1.2*IMC)+(0.23*edad)-5.4
        IMCIdeal = PesoIdeal/(AlturaM**2) 
        PorcentajeGrasaIdeal=(1.2*IMCIdeal)+(0.23*edad)-5.4
    
    kcalSedentario=BMR*1.53
    kcalActivo=BMR*1.76
    kcalVActivo=BMR*2.25
    
    
    with st.expander("EVALUACIÓN DE SALUD"):
        st.subheader("VALORES DE REFERENCIA")
        col1, col2, col3 = st.columns(3)
        col1.metric("PESO IDEAL", "{0:.0f}".format(PesoIdeal) + str(" kg") )
        col2.metric("IMC IDEAL", '{0:.0f} '.format(IMCIdeal))
        col3.metric("GRASA CORPORAL IDEAL", str(int(PorcentajeGrasaIdeal))+"%")
        #col4.metric("CLASIFICACIÓN", "NORMAL")
        st.subheader("ESTADO DE SALUD : " +  Estado)
        col1, col2, col3  = st.columns(3)
        col1.metric("PESO ACTUAL", "{0:.0f}".format(peso) + str(" kg") )
        col2.metric("IMC", '{0:.0f} '.format(IMC))
        col3.metric("GRASA CORPORAL", str(int(PorcentajeGrasa))+"%")
        #col4.metric("CLASIFICACIÓN", Estado)
        st.subheader("NECESIDADES CALORICAS")
        col1, col2, col3 = st.columns(3)
        col1.metric("SEDENTARIO (kcal)", '{0:.0f} '.format(kcalSedentario))
        col2.metric("ACTIVO (kcal) ", '{0:.0f}' .format(kcalActivo))
        col3.metric("VIGOROSO (kcal)", '{0:.0f}'.format(kcalVActivo))
    
    
    
    
    with st.expander("PRONOSTICO DE VARIACIÓN DE PESO PARA LA DIETAS PROPUESTA SEGUN EL RÉGIMEN DE ACTIVIDAD"):
        opciones_de_regimenes = ['SEDENTARIO', 'ACTIVO', 'VIGOROSAMENTE ACTIVO']
        opciones = st.multiselect(
            'SELECCIONE REGIMENES DE ACTIVIDAD',
            opciones_de_regimenes)
        
        if len(opciones) > 0:
            x = np.linspace(0, 30, 500)
            y = np.ones(500)
            
            fig1, ax1 = plt.subplots()
            
            for funcion in opciones:                
                if funcion == 'SEDENTARIO':
                    Gasto = kcalSedentario
                    y = vpeso/30 * x+peso
                    ax1.plot(x, y, 'b--', label='Dieta Regimenes Sedentario, Activo, Vigorosamente Activo ')
                elif funcion == 'ACTIVO':
                    GastoActivo=kcalActivo-kcalSedentario
                    y = vpeso/30 * x+peso-GastoActivo/9000 * x
                    ax1.plot(x, y, 'r--', label='Dieta Sedentaria con Regimen Activo')
                elif funcion == 'VIGOROSAMENTE ACTIVO':
                    GastoVActivo=kcalVActivo-kcalSedentario
                    y = vpeso/30 * x+peso-GastoVActivo/9000 * x
                    ax1.plot(x, y, 'g--', label='Dieta Sedentaria con Regimen Vigorosamente Activo')
        
            ax1.grid()
            ax1.legend(loc='best')
            vtitle = "Proyección de variación de Peso"
            xtitle = "Tiempo(dias)"
            ytitle = "Peso (kg)"
            ax1.set(xlabel=xtitle, ylabel=ytitle,title= vtitle)

            st.pyplot(fig1)
    
            Boton_Proyeccion = st.button('Salvar  Gráfico')
    
            if Boton_Proyeccion == True:
               fig1.savefig(vtitle + str(fecha) + ".png")
                
            Boton_Proyeccion = False
    
        
        limite=12    
        
    with st.expander("SELECCIÓN DE ALIMENTOS"):
        TSeleccion = st.radio("TIPO DE SELECCIÓN",
     ('DEFAULT','PERSONALIZADA','PERSONALIZAR'))
        if TSeleccion == 'DEFAULT':
            p_dataframe = pd.read_csv(directory +"/default_data/Proteinas.csv")
            c_dataframe = pd.read_csv(directory +"/default_data/Carbohidratos.csv")
            indice = 0
            col1, col2 = st.columns(2)
            with col1:
                if p_dataframe is not None:
                    st.write("Proteina Cargada ")
                    boton_izquierdo = st.button('Visualizar',
                                                key="left_v/o")
                    if boton_izquierdo:
                        st.dataframe(p_dataframe)
                        boton_izquierdo = False
                    
            with col2:
                if c_dataframe is not None:
                    st.write("Carbohidrato Cargados ")
                    boton_derecho = st.button('Visualizar',
                                                key="right_v/o")
                    
                    if boton_derecho:
                        st.dataframe(c_dataframe)
                        boton_derecho = False
                    
                
            
        elif TSeleccion == 'PERSONALIZADA':
            col1, col2 = st.columns(2)
            with col1:
                st.header("PROTEINAS")
                P_uploaded_file = st.file_uploader(" ",key="p_upload")
                if P_uploaded_file is not None:
                    p_dataframe = pd.read_csv(P_uploaded_file)
                    st.dataframe(p_dataframe)
            with col2:
                st.header("CARBOHIDRATOS")
                C_uploaded_file = st.file_uploader(" ",key="c_upload")
                if C_uploaded_file is not None:
                    c_dataframe = pd.read_csv(C_uploaded_file)
                    st.write(c_dataframe)
            
            if P_uploaded_file is not None and C_uploaded_file is not None:
                st.write(c_dataframe.Nombre)
                st.write(type(c_dataframe.loc[0]))
            
            
        elif TSeleccion == 'PERSONALIZAR':
            col1, col2 = st.columns(2)
            with col1:
                st.header("PROTEINAS")
                P_uploaded_file = st.file_uploader(" ",key="p_upload")
                if P_uploaded_file is not None:
                    p_dataframe = pd.read_csv(P_uploaded_file)
                    st.dataframe(p_dataframe)
            with col2:
                st.header("CARBOHIDRATOS")
                C_uploaded_file = st.file_uploader(" ",key="c_upload")
                if C_uploaded_file is not None:
                    c_dataframe = pd.read_csv(C_uploaded_file)
                    st.write(c_dataframe)
        
    
    with st.expander("NUEVO CALCULO DIETA"):
        R_actividad_fisica = st.radio("SELECCION DE RÉGIMEN DE ACTIVIDAD FÍSICA", ('SEDENTARIO', 'ACTIVO','VIGOROSAMENTE ACTIVO'),key="ACTIVIDAD")
        if R_actividad_fisica == 'SEDENTARIO':
            Gasto = kcalSedentario
        elif R_actividad_fisica == 'ACTIVO':
            Gasto = kcalActivo
        elif R_actividad_fisica == 'VIGOROSAMENTE ACTIVO':
            Gasto = kcalVActivo
        agree = st.checkbox('CALCULAR')
        if agree:
            columna_nombre_proteina, columna_masa_proteina, columna_nombre_carbohidrato, columna_masa_carbohidrato_almuerzo, columna_masa_carbohidrato_comida = dcalculo(peso,Gasto,vpeso,p_dataframe,c_dataframe)
        
            
            mydataset = {
                'Proteína': columna_nombre_proteina,
                '    (g) ': columna_masa_proteina,
                'Carbohidrato': columna_nombre_carbohidrato,
                'Almuerzo': columna_masa_carbohidrato_almuerzo,
                'Comida': columna_masa_carbohidrato_comida                
            }
            
            myvar = pd.DataFrame(mydataset)
            
            
            st.write('CALCULO COMPLETADO')            
            
            
            
            view = st.checkbox('Visualizar')
            if view:
                st.dataframe(myvar)
            
            col1, col2 = st.columns(2)
            with col1:
                g_repor = st.checkbox('Generar Informe')
                if g_repor:
                    archivo =  nombre + '-' +str(fecha) + '.tex'
                    Tabla = "Tabla_" + nombre + '-' +str(fecha) + '.pdf'
                    archivopdf = nombre + '-' +str(fecha) + '.pdf'
                    down_archivo_pdf = directory + "/" + archivopdf
                    
                    #-------------------------------------------
                    
                    fig, ax =plt.subplots(figsize=(30,6))#figsize=(12,4)
                    ax.axis('tight')
                    ax.axis('off')
                    the_table = ax.table(cellText=myvar.values,
                                         colLabels=myvar.columns,
                                         fontsize=30,
                                         loc='center')
                    pp = PdfPages(Tabla)
                    pp.savefig(fig, bbox_inches='tight'),#
                    pp.close()
                    
                    #-------------------------------------------
                    #st.write(preheader+header.format('Hola'))
                    
                    #header = """\documentclass{article}
                    #    
                    ##    \\begin{document}
                    # 
                    ##     """
                        
                    
                    
                    
                    
                    #footer = """
                    #    
                    #    First document. This is a simple example, with no 
                    #    extra parameters or packages included.
                    #    \end{document}
                    #    """
                        
                    #content = header +   footer

                    #content = header + main +  footer
                        
                    #with open(archivo,'w') as f:
                    #    f.write(content)
                            
                        
                    #os.system("pdflatex {fname}".format(fname = archivo))
                    
                    
                    
                
            with col2:
                @st.cache
                def convert_df(df):
                    # IMPORTANT: Cache the conversion
                    #to prevent computation on every rerun
                    return df.to_csv().encode('utf-8')
                
                csv = convert_df(myvar)
                
                st.download_button(label="Descargar  como CSV",
                                   data=csv,
                                   file_name="Dieta-"+ nombre  + "-" +
                               str(fecha)+'.csv',
                                   mime='text/csv',
                                  )
                #down = st.checkbox('Descargar')
                #if down:
                    
                #    st.write("Descargado")
                    


Test = st.checkbox('TEST')

if Test:
    #with open('prueba.tex','w') as f:
    #    f.write(article)
    #    f.write(plantilla)

    #st.write(plantilla)

    #st.write(preheader)
    st.write(create_preheader('Analisis de la dieta', 'Henry Hodelin Shombert'))


    
    #os.system("pdflatex {fname}".format(fname = "prueba.tex"))        
    

    


    