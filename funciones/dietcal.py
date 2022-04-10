import streamlit as st


def greeting(name):
    return "Hello, " + name


@st.cache
def dcalculo(peso,Gasto,vpeso,p_dataframe,c_dataframe):
    PProteina=peso*1.2/2 
    Dieta=round(Gasto + vpeso*300)
    Desayuno=round(Dieta*0.2)
    Merienda=round(Dieta*0.05)
    Almuerzo=round(Dieta*0.35)
    MeriendaT=round(Dieta*0.1)
    Comida=round(Dieta*0.3)
            
    columna_nombre_proteina = []
    columna_masa_proteina = []
    columna_nombre_carbohidrato = []
    columna_masa_carbohidrato_almuerzo = []
    columna_masa_carbohidrato_comida = []
            
            


            
    for p_row in p_dataframe.itertuples(index=False):
        Nombre_Proteina =  p_row[0] + "  "
        Contenido_Proteico_Proteina = p_row[1]
        Valor_Calorico_Proteina =  p_row[2]
                
        Masa_Proteina = int((PProteina*100)/Contenido_Proteico_Proteina)
        KCal_Proteina = int((Valor_Calorico_Proteina*Masa_Proteina)/100) 
        KCal_Carbohidratos_Almuerzo = int(Almuerzo) - KCal_Proteina
        KCal_Carbohidratos_Comida = int(Comida) - KCal_Proteina
                
                
        for c_row in c_dataframe.itertuples(index=False):
            Nombre_Carbohidrato =  c_row[0] + "  "
            Contenido_Proteico_Carbohidrato = c_row[1]
            Valor_Calorico_Carbohidrato =  c_row[2]
                    
            if KCal_Carbohidratos_Almuerzo > 0:
                Masa_Carbohidratos_Almuerzo = str(int((KCal_Carbohidratos_Almuerzo*100)/Valor_Calorico_Carbohidrato)) + " g"
            else: 
                Masa_Carbohidratos_Almuerzo = "Combinación no apropiada"
            if KCal_Carbohidratos_Comida > 0:
                Masa_Carbohidratos_Comida = str( int((KCal_Carbohidratos_Comida*100)/Valor_Calorico_Carbohidrato)) + " g"
            else: 
                Masa_Carbohidratos_Comida = "Combinación no apropiada"
                    
                    
                    
                columna_nombre_proteina.append(Nombre_Proteina)
                columna_masa_proteina.append(str(Masa_Proteina))
                columna_nombre_carbohidrato.append(Nombre_Carbohidrato)
                columna_masa_carbohidrato_almuerzo.append(Masa_Carbohidratos_Almuerzo)
                columna_masa_carbohidrato_comida.append(Masa_Carbohidratos_Comida)

    return  columna_nombre_proteina, columna_masa_proteina, columna_nombre_carbohidrato, columna_masa_carbohidrato_almuerzo, columna_masa_carbohidrato_comida
                
  