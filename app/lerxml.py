import os
import xmltodict
from dictor import dictor


diretorio_xml = 'C:\\xml\\25052368000124_55_01022025_28022025\\prod\\'
arquivos_no_diretorio = os.listdir(diretorio_xml)
arquivos_xml= [arquivo for arquivo in arquivos_no_diretorio if arquivo.endswith('.xml')]
contador=0
evento=0
cancelamento=0
intutilizacao =0

ufporFaturamento ={}
def enviaUFxFaturamentoNFe(UF, TotalNFe):
   if UF in ufporFaturamento:
      ufporFaturamento[UF] +=TotalNFe
   else:
      ufporFaturamento[UF] = TotalNFe

def enviadictufporFaturamento():
   return ufporFaturamento



if not arquivos_xml:
    print('Nenhum arquivo XML encontrado no diretório atual.')
else:
    for nome_arquivo in arquivos_xml:
        caminho_arquivo = os.path.join(diretorio_xml, nome_arquivo)
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
             conteudo_xml = arquivo.read()
        dados = xmltodict.parse(conteudo_xml)
   
        #print("Dados lidos:", dados)
        #print(json.dumps(dados, indent=4, ensure_ascii=False))
        
        proc =  dictor(dados, 'procEventoNFe')
        tipoEventoCancelamento = dictor(dados,'procEventoNFe.retEvento.infEvento.xEvento')
        tipoEventointutilizacao = dictor(dados,'ProcInutNFe.retInutNFe.infInut.xMotivo')
        if 'Cancelamento' in str(tipoEventoCancelamento):
          cancelamento+=1
          evento+=1
          continue
        elif 'Inutilização de número homologado' in str(tipoEventointutilizacao):
          intutilizacao +=1
          evento+=1
          continue
        else: 
          cpf_cnpj_emitente = dictor(dados, 'nfeProc.NFe.infNFe.dest.CPF')
          if not cpf_cnpj_emitente:
            cpf_cnpj_emitente = dictor(dados, 'nfeProc.NFe.infNFe.dest.CNPJ')
            contador+=1
          uf = dictor(dados, 'nfeProc.NFe.infNFe.dest.enderDest.UF')   
          chave =  dictor(dados, 'nfeProc.NFe.infNFe.@Id') 
          #print(chave) 
          #print(nome_arquivo)
          vNF = float(dictor(dados, 'nfeProc.NFe.infNFe.total.ICMSTot.vNF'))
          enviaUFxFaturamentoNFe(uf,vNF)
         

    #print(f"CNPJ do Destinatário: {cpf_cnpj_emitente}")
    print('Quantidade de NFCe ',contador)
    print('Quantidade de Cancelamentos ',cancelamento)
    print('Quantidade de Inutilizadas ',intutilizacao)
    print('Quantidade de Eventos ',evento)
    print('Total de arquivos {}'.format(contador + cancelamento + intutilizacao))
    print(enviadictufporFaturamento())



   