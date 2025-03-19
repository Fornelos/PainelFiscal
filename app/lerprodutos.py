import os
import xmltodict
from dictor import dictor
import json
from collections import OrderedDict

produto={}
diretorio_xml = 'C:\\xml\\25052368000124_55_01022025_28022025\\prod\\'
arquivos_no_diretorio = os.listdir(diretorio_xml)
arquivos_xml= [arquivo for arquivo in arquivos_no_diretorio if arquivo.endswith('procNFe.xml')]

def insereProduto(codigo,descricao,quantidade):
   if codigo in produto:
    produto[codigo]['Quantidade'] +=float(quantidade)
   else:
    produto[codigo] = {
    'Descricao':descricao, 
    'Quantidade': float(quantidade)
    }

def ordenaDescricao(dicionario):
   produtos_ordenados_descricao = dict(sorted(dicionario.items(), key=lambda item: item[1]['Descricao']))
   return produtos_ordenados_descricao


def ordenaQuantidadeDesc(dicionario):
   produtos_ordenados_quantidade_decrescente = dict(sorted(dicionario.items(), key=lambda item: item[1]['Quantidade'], reverse=True))
   ordemQuantidade_json_formatado = json.dumps(produtos_ordenados_quantidade_decrescente, indent=4, ensure_ascii=False, sort_keys=True)
   print(ordemQuantidade_json_formatado)

   
   

   

if not arquivos_xml:
    print('Nenhum arquivo XML encontrado no diretório atual.')
else:
    for nome_arquivo in arquivos_xml:
        caminho_arquivo = os.path.join(diretorio_xml, nome_arquivo)
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
             conteudo_xml = arquivo.read()
        dados = xmltodict.parse(conteudo_xml)
        det_prod1 = dictor(dados, 'nfeProc.NFe.infNFe.det')

        proc =  dictor(dados, 'procEventoNFe')
        tipoEventoCancelamento = dictor(dados,'procEventoNFe.retEvento.infEvento.xEvento')
        tipoEventointutilizacao = dictor(dados,'ProcInutNFe.retInutNFe.infInut.xMotivo')
        if 'Cancelamento' in str(tipoEventoCancelamento):
          continue
        elif 'Inutilização de número homologado' in str(tipoEventointutilizacao):
          continue
        else: 
             # Verifica se det_prod1 é uma lista antes de iterar
         if det_prod1 and isinstance(det_prod1, list):
            for item in det_prod1:
                  if isinstance(item, dict) and 'prod' in item:
                    codigo_produto = item['prod']['cProd']
                    quantidade = item['prod']['qCom']
                    descricao = item['prod']['xProd']
                    insereProduto(codigo_produto,descricao,quantidade)
                    
         else:
            codigo_produto  = dictor(det_prod1,'prod.cProd')
            quantidade = dictor(det_prod1,'prod.qCom')
            descricao = dictor(det_prod1,'prod.xProd')
            insereProduto(codigo_produto,descricao,quantidade)

json_formatado = json.dumps(produto, indent=4, ensure_ascii=False, sort_keys=True)
#print(json_formatado)
#print(len(produto))
ordemQuantidade = ordenaQuantidadeDesc(produto)

