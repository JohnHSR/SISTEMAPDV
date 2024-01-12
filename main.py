from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QMessageBox, QAbstractItemView
from PySide6.QtCore import Qt, QTimer, QDate
from PySide6.QtGui import QPixmap
import sys, json
from datetime import timedelta, datetime



versao = "1.0"
data_e_hora_atuais = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
operador = "John"
cliente_padrao = "Cliente Padrao"
mensagem_status = f"{data_e_hora_atuais} - Operador: {operador}                          Sistema - Versão {versao} - Em desenvolvimento por: John H."


# Definindo o atributo antes de criar a QApplication
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.loader = QUiLoader()
        self.atualizar_layout_inicial()
        self.resize(1400,715)
        
        self.lista_produtos = []
        self.pedido = {}
        self.lista_cad_clientes = []
        self.acessorios_incluidos = []

        ## BARRA DE STATUS =============================================================================================
        barra_status = self.statusBar()
        barra_status.showMessage(mensagem_status)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_hora)
        self.timer.start(1) # Timer definido para 1000 ms (1 segundo)
        fonte_barra_status = barra_status.font()
        fonte_barra_status.setPointSize(10)
        fonte_barra_status.setBold(True)
        barra_status.setFont(fonte_barra_status)

##############################################################################################################        
        
    def config_padrao(self):
        
        if hasattr(self.ui, 'label_pixmap'):
            # Imagem da tela inicial
            imagem = QPixmap('imagens/logo.png')
            label_imagem = self.ui.label_pixmap
            label_imagem.setScaledContents(True)
            label_imagem.setPixmap(imagem)
             
        
        if hasattr(self.ui, 'botao_home'):
            self.ui.botao_home.disconnect(self)
            self.ui.botao_home.clicked.connect(self.atualizar_layout_inicial)

        # Sinais
        if hasattr(self.ui, 'acao_estoque_produtos'):
            self.ui.acao_estoque_produtos.disconnect(self)
            self.ui.acao_estoque_produtos.triggered.connect(self.atualizar_layout_estoque_produtos)
            self.ui.acao_estoque_produtos.setShortcut('F2')
            
        
        if hasattr(self.ui, 'acao_realizar_venda'):
            self.ui.acao_realizar_venda.disconnect(self)
            self.ui.acao_realizar_venda.triggered.connect(self.atualizar_layout_realizar_vendas)
            self.ui.acao_realizar_venda.setShortcut('F1')
            


        if hasattr(self.ui, 'acao_consultar_vendas'):
            self.ui.acao_consultar_vendas.disconnect(self)
            self.ui.acao_consultar_vendas.triggered.connect(self.atualizar_layout_pedidos)
            self.ui.acao_consultar_vendas.setShortcut('F3')
            
        if hasattr(self.ui, 'acao_cadastro_clientes'):
            self.ui.acao_cadastro_clientes.disconnect(self)
            self.ui.acao_cadastro_clientes.triggered.connect(self.atualizar_layout_cadastro_clientes)
            self.ui.acao_cadastro_clientes.setShortcut('F4')
            
        if hasattr(self.ui, 'acao_nova_os'):
            self.ui.acao_nova_os.disconnect(self)
            self.ui.acao_nova_os.triggered.connect(self.atualizar_layout_nova_os)
            self.ui.acao_nova_os.setShortcut('F5')
            
    def atualizar_hora(self):
        data_e_hora_atuais = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        mensagem_status = f"{data_e_hora_atuais} - Operador: {operador}                          Sistema - Versão {versao} - Em desenvolvimento por: John H."
        self.statusBar().showMessage(mensagem_status)   

##############################################################################################################

    def atualizar_layout_inicial(self):
        self.ui = self.loader.load("Layout/tela_inicial.ui")
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Sistema de Vendas")
        
        self.config_padrao()
             
##############################################################################################################         
        
    def atualizar_layout_realizar_vendas(self):
        self.ui = self.loader.load("Layout/tela_realizar_venda.ui")
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Sistema de Vendas - Realizar Venda")
        
        self.config_padrao()
        
        ## Campos
        
        botao_home = self.ui.botao_home
        label_codigo_produto = self.ui.vendas_label_codigo_produto
        input_codigo_produto = self.ui.vendas_input_produto
        input_quantidade_produto = self.ui.vendas_quantidade_produto
        campo_nome_produto = self.ui.vendas_nome_produto
        campo_valor_produto = self.ui.vendas_valor_produto
        label_estoque_produto = self.ui.vendas_estoque
        campo_quantidade_estoque = self.ui.vendas_qtd_estoque
        label_localizacao_produto = self.ui.vendas_label_localizacao
        campo_localizacao = self.ui.vendas_localizacao_prod
        label_referencia_produto = self.ui.vendas_label_referencia
        campo_referencia = self.ui.vendas_referencia_prod
        label_unidade_produto = self.ui.vendas_label_unidade
        campo_unidade = self.ui.vendas_unidade_prod
        campo_observacao_produto = self.ui.vendas_observ_prod
        label_total_produto = self.ui.vendas_label_total_produto
        campo_total_produto = self.ui.vendas_total_produto
        botao_adicionar_produto = self.ui.vendas_adicionar_produto
        
        cupom_pedido = self.ui.vendas_cupom
        botao_limpar_pedido = self.ui.vendas_limpar_pedido
        
        label_formas_pgto = self.ui.vendas_label_formas_pgto
        radio_dinheiro = self.ui.vendas_pgto_din
        radio_pix = self.ui.vendas_pgto_pix
        radio_credito = self.ui.vendas_pgto_cre
        radio_debito = self.ui.vendas_pgto_deb
        radio_pos = self.ui.vendas_pgto_pos
        
        botao_selecionar_cliente = self.ui.vendas_selecionar_cliente
        botao_cliente_padrao = self.ui.vendas_cliente_padrao
        label_cliente = self.ui.vendas_label_cliente
        campo_cliente = self.ui.vendas_cliente
        
        label_parcelas = self.ui.vendas_label_parcelas
        campo_parcelas = self.ui.vendas_qtdade_parcelas
        
        label_desconto = self.ui.vendas_label_desconto
        campo_valor_desconto = self.ui.vendas_valor_desconto
        campo_porc_desconto = self.ui.vendas_porc_desconto
        
        label_adicional = self.ui.vendas_label_adicional
        campo_valor_adicional = self.ui.vendas_valor_adicional
        campo_porc_adicional = self.ui.vendas_porc_adicional
        
        label_total_pedido = self.ui.vendas_label_total
        campo_total_pedido = self.ui.vendas_total_pedido
        
        botao_fechar_pedido = self.ui.vendas_fechar_pedido
        
        ## Configs
        campo_parcelas.setVisible(False)
        label_parcelas.setVisible(False)
        
        ## Métodos
        
        class Produto():
            
            def __init__(self):
                pass
            
            def somar_total_pedido():
                
                global valor_adicional
                global valor_desconto
                
                total_pedido = 0
                for produto in self.lista_produtos:
                    total_produto = produto['Valor Total']
                    total_produto = total_produto.replace("R$ ", "").replace(",", ".")
                    total_pedido += float(total_produto)
                
                valor_desconto = (campo_porc_desconto.value() * total_pedido / 100 ) + (campo_valor_desconto.value())
                valor_adicional = (campo_porc_adicional.value() * total_pedido / 100) + (campo_valor_adicional.value())
                
                total_pedido = total_pedido - valor_desconto + valor_adicional
                
                campo_total_pedido.setText(f"R$ {total_pedido:.2f}".replace(".", ","))

            def atualizar_dados_produto(cod_produto):
                with open("dados/produtos_temp.json", "r") as arquivo:
                    produtos = json.load(arquivo)
                    
                for registro in produtos['produtos']:
                    if cod_produto == registro['Codigo do produto']:
                        campo_nome_produto.setText(registro['Nome do produto'])
                        campo_valor_produto.setText(f"R$ {registro['Valor Unitario']}".replace(".", ","))
                        campo_quantidade_estoque.setText(str(registro['Quantidade em estoque']))
                        campo_localizacao.setText(registro['Localizacao do produto'])
                        campo_referencia.setText(registro['Referencia'])
                        campo_unidade.setText(registro['Unidade'])
                        campo_observacao_produto.setText(registro['Observacao livre'])
                        
                        quantidade = input_quantidade_produto.value()
                        valor = float(campo_valor_produto.text().replace("R$ ", "").replace(",", "."))
                        total = quantidade * valor
                        campo_total_produto.setText(f"R$ {total:.2f}".replace(".", ","))
                        
                        return None
                    else:
                        campo_nome_produto.setText("---------------------------")
                        campo_valor_produto.setText("R$ 0,00")
                        campo_quantidade_estoque.setText("---")
                        campo_localizacao.setText("---")
                        campo_referencia.setText("---")
                        campo_unidade.setText("---")
                        campo_observacao_produto.setText("---")
                        campo_total_produto.setText("R$ 0,00")

            def adicionar_produto_cupom():
                with open("dados/produtos_temp.json", "r") as arquivo:
                    produtos = json.load(arquivo)
                    
                for registro in produtos['produtos']:
                    if input_codigo_produto.text() == registro['Codigo do produto']:
                        codigo_produto = registro['Codigo do produto']
                        nome_produto = registro['Nome do produto']
                        estoque = registro['Quantidade em estoque']
                        quantidade = input_quantidade_produto.value()
                        valor_unitario = registro['Valor Unitario']
                        valor_total = quantidade * valor_unitario
                        valor_total = f"R$ {valor_total:.2f}".replace(".", ",")
                        produto_encontrado = True
                        break
                    else:
                        produto_encontrado = False
                        
                if produto_encontrado == False:
                    QMessageBox.warning(self, "Erro", "Produto não encontrado!")
                    return None
                
                if quantidade > estoque:
                    QMessageBox.warning(self, "Erro", "Quantidade maior que o estoque!")
                    campo_quantidade_estoque.setValue(1)
                    return None
                
                # Atualizar estoque do produto
                for registro in produtos['produtos']:
                    if input_codigo_produto.text() == registro['Codigo do produto']:
                        if str(registro['Quantidade em estoque']).endswith(".0") and str(quantidade).endswith(".0"):
                            estoque_novo = int(registro['Quantidade em estoque']) - int(quantidade)
                            registro['Quantidade em estoque'] = estoque_novo
                        else:
                            estoque_novo = float(registro['Quantidade em estoque']) - float(quantidade)
                            registro['Quantidade em estoque'] = estoque_novo
                            
                with open ("dados/produtos_temp.json", "w") as arquivo:
                    json.dump(produtos, arquivo, indent=4)
                
                produto = {
                    'Codigo do produto': codigo_produto,
                    'Nome do produto': nome_produto,
                    'Quantidade': quantidade,
                    'Valor Unitario': valor_unitario,
                    'Valor Total': valor_total
                }
                
                self.lista_produtos.append(produto)
                
                produto = f"""
                    <h2 style="text-align: center;"><strong>{codigo_produto} -&nbsp;{nome_produto}&nbsp; &nbsp;</strong></h2>

                    <p style="text-align: center;"><strong>QUANTIDADE: {quantidade}</strong></p>

                    <p style="text-align: center;"><strong>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; VALOR UNITARIO: {valor_total}</strong></p>

                    <p style="text-align: center;"><strong>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;VALOR TOTAL: {valor_total}</strong></p>
                    
                    <h2 style="text-align:center"><strong>============================</strong></h2>
                    
                    <p>&nbsp;</p>
                    
                """  
                cupom_pedido.append(produto)
                
                self.pedido['Numero do pedido'] = ''
                self.pedido['Data e hora'] = ''
                self.pedido['Operador'] = ''
                self.pedido['Cliente'] = campo_cliente.text()
                self.pedido['Produtos'] = self.lista_produtos
                self.pedido['Forma de pagamento'] = ""
                self.pedido['Quantidade de parcelas'] = ''
                self.pedido['Desconto'] = ''
                self.pedido['Acrescimo'] = ''
                self.pedido['Valor total'] = ''
                
                with open("dados/pedido_temp.json", "w") as arquivo:
                    json.dump(self.pedido, arquivo, indent=4)
                
                
                input_codigo_produto.setText("")
                input_quantidade_produto.setValue(1)
                campo_nome_produto.setText("---------------------------")
                campo_valor_produto.setText("R$ 0,00")
                campo_quantidade_estoque.setText("---")
                campo_localizacao.setText("---")
                campo_referencia.setText("---")
                campo_unidade.setText("---")
                campo_observacao_produto.setText("---")
                campo_total_produto.setText("R$ 0,00")
                
                Produto.somar_total_pedido()
            
            def ultimo_numero_pedido():
                with open("dados/pedidos.json", "r") as arquivo:
                    pedidos = json.load(arquivo)
                
                if pedidos['pedidos'] == [] or pedidos['pedidos'] is None:
                    return 1
                
                else:
                    return pedidos['pedidos'][-1]['Numero do pedido'] + 1
                
            def baixar_produtos_estoque(codigo):
                with open("dados/pedido_temp.json", "r") as arquivo:
                    pedido_temp = json.load(arquivo)
                
                with open("dados/produtos.json", "r") as arquivo:
                    produtos = json.load(arquivo)
                
                for produto in pedido_temp['Produtos']:
                    for registro in produtos['produtos']:
                        if produto['Codigo do produto'] == registro['Codigo do produto']:
                            # Se a quantidade for inteira, subtrai normalmente
                            if str(registro['Quantidade em estoque']).endswith(".0") and str(produto['Quantidade']).endswith(".0"):
                                estoque_novo = int(registro['Quantidade em estoque']) - int(produto['Quantidade'])
                                registro['Quantidade em estoque'] = estoque_novo
                            else:
                                estoque_novo = float(registro['Quantidade em estoque']) - float(produto['Quantidade'])
                                registro['Quantidade em estoque'] = estoque_novo                                
                                
                                
                
                with open ("dados/produtos.json", "w") as arquivo:
                    json.dump(produtos, arquivo, indent=4)
                
            def finalizar_pedido():
                try:
                    with open("dados/pedido_temp.json", "r") as arquivo:
                        pedido_temp = json.load(arquivo)
                        
                    if pedido_temp == {} or pedido_temp is None:
                        QMessageBox.warning(self, "Erro", "Nenhum pedido para ser fechado!")
                        return None
                    
                    if self.lista_produtos == []:
                        QMessageBox.warning(self, "Erro", "Nenhum produto adicionado ao pedido!")
                        return None
                    
                    if radio_dinheiro.isChecked():
                        forma_pgto = "Dinheiro"
                    elif radio_pix.isChecked():
                        forma_pgto = "Pix"
                    elif radio_credito.isChecked():
                        forma_pgto = "Credito"
                    elif radio_debito.isChecked():
                        forma_pgto = "Debito"
                    elif radio_pos.isChecked():
                        forma_pgto = "Postergar"
                        
                    if forma_pgto == "Dinheiro":
                        self.ui2 = self.loader.load("Layout/tela_troco.ui")
                        self.ui2.show()
                        
                        self.ui2.troco_campo_vlrped.setText(campo_total_pedido.text())
                        valor_pedido = campo_total_pedido.text().replace("R$ ", "").replace(",", ".")
                        
                        
                        def calcular_troco():
                            valor_pago = self.ui2.troco_campo_vlrpag.text().replace(',', '.')
                            if valor_pago == "" or valor_pago.isnumeric() == False:
                                valor_pago = 0
                                return None
                            troco = float(valor_pago) - float(valor_pedido)
                            self.ui2.troco_campo_vlrtroc.setText(f"R$ {troco:.2f}".replace(".", ","))
                            
                        def finalizar():
                            numero_parcelas = 1
                            for produto in self.lista_produtos:
                                Produto.baixar_produtos_estoque(produto['Codigo do produto'])
                                
                            numero_pedido = Produto.ultimo_numero_pedido()
                            
                            self.pedido['Numero do pedido'] = numero_pedido
                            self.pedido['Data e hora'] = data_e_hora_atuais
                            self.pedido['Operador'] = operador
                            self.pedido['Cliente'] = campo_cliente.text()
                            self.pedido['Produtos'] = self.lista_produtos
                            self.pedido['Forma de pagamento'] = forma_pgto
                            self.pedido['Quantidade de parcelas'] = numero_parcelas
                            self.pedido['Desconto'] = f"R$ {valor_desconto:.2f}".replace(".", ",")
                            self.pedido['Acrescimo'] = f"R$ {valor_adicional:.2f}".replace(".", ",")
                            self.pedido['Valor total'] = campo_total_pedido.text()
                            
                            with open("dados/pedidos.json", "r") as arquivo:
                                pedidos = json.load(arquivo)
                                
                            pedidos['pedidos'].append(self.pedido)
                            
                            with open("dados/pedidos.json", "w") as arquivo:
                                json.dump(pedidos, arquivo, indent=4)
                                
                            with open ("dados/pedido_temp.json", "w") as arquivo:
                                json.dump({}, arquivo, indent=4)
                                
                            self.pedido = {}
                            self.lista_produtos = []
                            
                            ## Sobrescrever os dados dos produtos pelos produtos temporários
                            with open("dados/produtos_temp.json", "r") as arquivo:
                                produtos_temp = json.load(arquivo)
                                
                            with open("dados/produtos.json", "w") as arquivo:
                                json.dump(produtos_temp, arquivo, indent=4)
                                
                            ###
                            
                            cupom = """
                            <html><head><meta name="qrichtext" content="1" /><style type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;">\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">-------------------------------------------------------------------------------------------------</span></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;"><br /></p>\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">SISTEMA DE VENDAS</span></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;"><br /></p>\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Razão Social da empresa</span></p>\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">CNPJ: 00.000.000/0001-00</span></p>\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">John H. (77) 90000-0000</span></p>\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Av. João Bobo Nº 000</span></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;"><br /></p>\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">----------------------------------------------------------------------------------------------</span></p></body></html>
                            """
                            
                            cupom_pedido.setText(cupom)
                            campo_total_pedido.setText("R$ 0,00")
                            return self.ui2.close(), QMessageBox.information(self, "Sucesso", f"Pedido {numero_pedido} finalizado com sucesso")
                        ## Sinais
                        self.ui2.troco_campo_vlrpag.textChanged.connect(calcular_troco)
                        self.ui2.troco_confirmar.clicked.connect(finalizar)

                    else:
                        if forma_pgto == "Credito":
                            numero_parcelas = campo_parcelas.value()
                        else:
                            numero_parcelas = 1 
                            
                        for produto in self.lista_produtos:
                            Produto.baixar_produtos_estoque(produto['Codigo do produto'])
                            
                        numero_pedido = Produto.ultimo_numero_pedido()
                        
                        self.pedido['Numero do pedido'] = numero_pedido
                        self.pedido['Data e hora'] = data_e_hora_atuais
                        self.pedido['Operador'] = operador
                        self.pedido['Cliente'] = campo_cliente.text()
                        self.pedido['Produtos'] = self.lista_produtos
                        self.pedido['Forma de pagamento'] = forma_pgto
                        self.pedido['Quantidade de parcelas'] = numero_parcelas
                        self.pedido['Desconto'] = f"R$ {valor_desconto:.2f}".replace(".", ",")
                        self.pedido['Acrescimo'] = f"R$ {valor_adicional:.2f}".replace(".", ",")
                        self.pedido['Valor total'] = campo_total_pedido.text()
                        
                        with open("dados/pedidos.json", "r") as arquivo:
                            pedidos = json.load(arquivo)
                            
                        pedidos['pedidos'].append(self.pedido)
                        
                        with open("dados/pedidos.json", "w") as arquivo:
                            json.dump(pedidos, arquivo, indent=4)
                            
                            
                        self.pedido = {}
                        self.lista_produtos = []
                        
                        ## Sobrescrever os dados dos produtos pelos produtos temporários
                        with open("dados/produtos_temp.json", "r") as arquivo:
                            produtos_temp = json.load(arquivo)
                            
                        with open("dados/produtos.json", "w") as arquivo:
                            json.dump(produtos_temp, arquivo, indent=4)
                            
                        ###
                        
                        QMessageBox.information(self, "Sucesso", f"Pedido {numero_pedido} finalizado com sucesso")
                        
                        with open ("dados/pedido_temp.json", "w") as arquivo:
                            json.dump({}, arquivo, indent=4)
                        
                        cupom = """
                        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><style type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;">\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">-------------------------------------------------------------------------------------------------</span></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;"><br /></p>\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">SISTEMA DE VENDAS</span></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;"><br /></p>\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Razão Social da empresa</span></p>\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">CNPJ: 00.000.000/0001-00</span></p>\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">John H. (77) 90000-0000</span></p>\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Av. João Bobo Nº 000</span></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;"><br /></p>\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">----------------------------------------------------------------------------------------------</span></p></body></html>
                        """
                        cupom_pedido.setText(cupom)
                        campo_total_pedido.setText("R$ 0,00")
                        
                except Exception as erro:
                    QMessageBox.warning(self, "Erro", f"Erro ao finalizar pedido: {erro}")
            
            def atualizar_dados_pedido_temp():
                with open("dados/pedido_temp.json", "r") as arquivo:
                    pedido_temp = json.load(arquivo)
                    
                if pedido_temp == {} or pedido_temp is None:
                    return None
                
                campo_cliente.setText(pedido_temp['Cliente'])
                
                self.lista_produtos = pedido_temp['Produtos']
                
                for produto in self.lista_produtos:
                    codigo_produto = produto['Codigo do produto']
                    nome_produto = produto['Nome do produto']
                    estoque = produto['Quantidade']
                    valor_unitario = produto['Valor Unitario']
                    valor_total = produto['Valor Total']
                    
                    produto = f"""
                    <h2 style="text-align: center;"><strong>{codigo_produto} -&nbsp;{nome_produto}&nbsp; &nbsp;</strong></h2>

                    <p style="text-align: center;"><strong>QUANTIDADE: {estoque}</strong></p>

                    <p style="text-align: center;"><strong>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; VALOR UNITARIO: {valor_total}</strong></p>

                    <p style="text-align: center;"><strong>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;VALOR TOTAL: {valor_total}</strong></p>
                    
                    <h2 style="text-align:center"><strong>==============================</strong></h2>
                    
                    <p>&nbsp;</p>
                    
                    """  
                    cupom_pedido.append(produto)
                    
                Produto.somar_total_pedido()
        
        Produto.atualizar_dados_pedido_temp() 
        
        def buscar_cliente(self):
            self.ui_buscar_cliente = self.loader.load("Layout/tela_buscar_cliente.ui")
            self.ui_buscar_cliente.setModal(True)
            self.ui_buscar_cliente.setFixedSize(self.ui_buscar_cliente.size())
            self.ui_buscar_cliente.show()
            
            campo_busca = self.ui_buscar_cliente.buscar_cliente_campo
            tabela = self.ui_buscar_cliente.buscar_cliente_tabela
            
            def atualizar_tabela_clientes():
                with open("dados/clientes.json", "r") as arquivo:
                    clientes = json.load(arquivo)
                    
                tabela.setRowCount(len(clientes['clientes']))
                tabela.setColumnCount(3)
                tabela.setHorizontalHeaderLabels(["Código", "Nome ou razão social", "CPF/CNPJ"])
                
                for i in range(len(clientes['clientes'])):
                    for j in range(3):
                        tabela.setItem(i, j, QTableWidgetItem(str(clientes['clientes'][i][list(clientes['clientes'][i].keys())[j]])))
                
                # Centralizar tudo
                for i in range(len(clientes['clientes'])):
                    for j in range(3):
                        tabela.item(i, j).setTextAlignment(Qt.AlignCenter)

                tabela.setEditTriggers(QTableWidget.NoEditTriggers)
                tabela.setSelectionMode(QAbstractItemView.SingleSelection)
            
                
                def filtrar_tabela(texto):
                    for i in range(len(clientes['clientes'])):
                        codigo_cliente = str(clientes['clientes'][i]['Codigo do cliente']).upper()
                        nome_razao = str(clientes['clientes'][i]['Nome ou razao social']).upper()
                        cpf_cnpj = str(clientes['clientes'][i]['CPF/CNPJ']).upper()
                        
                        if texto.upper() in codigo_cliente or texto.upper() in nome_razao or texto.upper() in cpf_cnpj:
                            tabela.setRowHidden(i, False)
                        else:
                            tabela.setRowHidden(i, True)
                
                def selecionar_cliente():
                    codigo_cliente = tabela.item(tabela.currentRow(), 0).text()
                    nome_cliente = tabela.item(tabela.currentRow(), 1).text()
                    
                    campo_cliente.setText(f"[{codigo_cliente}] - {nome_cliente}")
                    self.ui_buscar_cliente.close()
                
                tabela.doubleClicked.connect(lambda: selecionar_cliente())
                campo_busca.textChanged.connect(lambda: filtrar_tabela(campo_busca.text()))
            
            atualizar_tabela_clientes()
        ## Configs
        
        ## Sinais
        
        input_codigo_produto.textChanged.connect(lambda: Produto.atualizar_dados_produto(input_codigo_produto.text()))
        input_quantidade_produto.valueChanged.connect(lambda: Produto.atualizar_dados_produto(input_codigo_produto.text()))
        
        botao_adicionar_produto.clicked.connect(lambda: Produto.adicionar_produto_cupom())
        
        campo_valor_desconto.valueChanged.connect(lambda: Produto.somar_total_pedido())
        campo_porc_desconto.valueChanged.connect(lambda: Produto.somar_total_pedido())
        
        campo_valor_adicional.valueChanged.connect(lambda: Produto.somar_total_pedido())
        campo_porc_adicional.valueChanged.connect(lambda: Produto.somar_total_pedido())
        
        botao_selecionar_cliente.clicked.connect(lambda: buscar_cliente(self))        
        botao_cliente_padrao.clicked.connect(lambda: campo_cliente.setText("Cliente padrao"))
        
        botao_fechar_pedido.clicked.connect(lambda: Produto.finalizar_pedido())

##############################################################################################################   
            
    def atualizar_layout_estoque_produtos(self):
        self.ui = self.loader.load("Layout/tela_estoque_prod.ui")
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Sistema de Vendas - Estoque de Produtos")
        
        self.config_padrao()

        ## Campos
        
        botao_home = self.ui.botao_home
        label_codigo_produto = self.ui.estoque_label_codnome
        input_codigo_nome = self.ui.estoque_input_produtos
        tabela_produtos = self.ui.estoque_tabela_produtos
        
        with open ("dados/produtos.json", "r") as arquivo:
            produtos = json.load(arquivo)
            
        ## Tabela
        
        # Configurações da tabela    
        tabela_produtos.setRowCount(len(produtos['produtos']))
        tabela_produtos.setColumnCount(10)
        tabela_produtos.setHorizontalHeaderLabels(["Código", 
                                                   "Nome", 
                                                   "Quantidade estoque", "Quantidade ideal", 
                                                   "Localização", "Valor unitário", "Valor de aquisição",
                                                   "Unidade", "Referência", "Observação livre"])
        
        for i in range(len(produtos['produtos'])):
            for j in range(10):
                tabela_produtos.setItem(i, j, QTableWidgetItem(str(produtos['produtos'][i][list(produtos['produtos'][i].keys())[j]])))
                
        tabela_produtos.resizeColumnsToContents()
        
        tabela_produtos.setEditTriggers(QTableWidget.NoEditTriggers)
        
        ## Sinais
        
        # Ao clicar 2x no produto, automaticamente abre a tela de vendas
        
        def double_click_prod():
            self.atualizar_layout_realizar_vendas()
            self.ui.vendas_input_produto.setText(tabela_produtos.item(tabela_produtos.currentRow(), 0).text())
        
        def filtrar_tabela(texto):
            for i in range(len(produtos['produtos'])):
                codigo_produto = str(produtos['produtos'][i]['Codigo do produto']).upper()
                nome_produto = str(produtos['produtos'][i]['Nome do produto']).upper()
                localizacao_produto = str(produtos['produtos'][i]['Localizacao do produto']).upper()
                referencia_produto = str(produtos['produtos'][i]['Referencia']).upper()
                
                if texto.upper() in codigo_produto or texto.upper() in nome_produto or texto.upper() in localizacao_produto or texto.upper() in referencia_produto:
                    tabela_produtos.setRowHidden(i, False)
                else:
                    tabela_produtos.setRowHidden(i, True)
        
        tabela_produtos.doubleClicked.connect(lambda: double_click_prod())
        
        input_codigo_nome.textChanged.connect(lambda: filtrar_tabela(input_codigo_nome.text()))
        
##############################################################################################################

    def atualizar_layout_pedidos(self):
        self.ui = self.loader.load("Layout/tela_consulta_pedidos.ui")
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Sistema de Vendas - Consulta de Pedidos")        
        self.config_padrao()
        
        ## Campos
        
        botao_filtrar = self.ui.pedidos_filtrar
        botao_limpar_filtros = self.ui.pedidos_limpar_filtros
        
        tabela_pedidos = self.ui.pedidos_tabela_pedidos
        
        label_num_pedido = self.ui.pedidos_label_nro
        campo_num_pedido = self.ui.pedidos_nro_pedido
        
        label_cliente = self.ui.pedidos_label_cliente
        campo_cliente = self.ui.pedidos_nome_cliente
        
        label_operador = self.ui.pedidos_label_operador
        campo_operador = self.ui.pedidos_nome_operador
        
        label_data_hora = self.ui.pedidos_label_datahora
        campo_data_hora = self.ui.pedidos_datahora
        
        label_produtos_pedido = self.ui.pedidos_label_produtos
        tabela_produtos_pedido = self.ui.pedidos_tabela_produtos
        label_total_pedido = self.ui.pedidos_label_total_pedido
        campo_total_pedido = self.ui.pedidos_total_pedido
        
        ## Métodos
        
        def abrir_tela_filtros():
            
            global botao_filtro_ped_cancelar
            global botao_filtro_ped_filtrar
            
            self.ui2 = self.loader.load("Layout/tela_filtrar_pedidos.ui")
            self.ui2.setModal(True)
            self.ui2.setWindowFlag(Qt.WindowCloseButtonHint, False)
            self.ui2.show()
            
            
            
            label_num_ped = self.ui2.filtro_pedidos_label_numped
            num_ped_ini = self.ui2.filtro_pedidos_pedido_inicial
            num_ped_fin = self.ui2.filtro_pedidos_pedido_final
            checkbox_num_ped = self.ui2.filtro_pedidos_chk_nro_pedido
            
            label_nomcodcli = self.ui2.filtro_pedidos_label_nomcodcli
            nom_cod_cli = self.ui2.filtro_pedidos_cliente
            
            label_ope = self.ui2.filtro_pedidos_label_ope
            nom_ope = self.ui2.filtro_pedidos_operador
            
            label_vlrped = self.ui2.filtro_pedidos_label_vlrped
            vlr_ped_ini = self.ui2.filtro_pedido_vlr_ini
            vlr_ped_fin = self.ui2.filtro_pedido_vlr_fin
            checkbox_vlr_ped = self.ui2.filtro_pedidos_chk_valor
            
            label_datainicial = self.ui2.filtro_pedidos_label_datainicial
            label_datafinal = self.ui2.filtro_pedidos_label_datafinal
            checkbox_data = self.ui2.filtro_pedidos_chk_data
            data_inicial = self.ui2.filtro_pedidos_dataini
            data_final = self.ui2.filtro_pedidos_datafin
            
            botao_filtro_ped_filtrar = self.ui2.filtro_pedidos_filtrar
            botao_filtro_ped_cancelar = self.ui2.filtro_pedidos_cancelar
            
            def filtros():
                def pedidos():
                    if checkbox_num_ped.isChecked():
                        if num_ped_ini.text() == "" or num_ped_fin.text() == "":
                            QMessageBox.warning(self, "Erro", "Preencha o numero do pedido inicial e final!")
                            return None
                        else:
                            return [int(num_ped_ini.text()), int(num_ped_fin.text())]
                    else:
                        if num_ped_ini.text() == "":
                            return None
                        else:
                            return [int(num_ped_ini.text())]
                        
                num_pedidos = pedidos()
                
                def cliente():
                    if nom_cod_cli.text() == "":
                        return None
                    else:
                        return nom_cod_cli.text()    
            
                nom_cliente = cliente()
                
                def operador():
                    if nom_ope.text() == "":
                        return None
                    else:
                        return nom_ope.text()
                    
                nom_operador = operador()
                
                def valor_pedido():
                    if checkbox_vlr_ped.isChecked():
                        if vlr_ped_ini.value() == 0.00 or vlr_ped_fin.value() == 0.00:
                            QMessageBox.warning(self, "Erro", "Preencha o valor inicial e final!")
                            return None
                        else:
                            return [float(vlr_ped_ini.value()), float(vlr_ped_fin.value())]
                    else:
                        if vlr_ped_ini.value() == 0.00:
                            return None
                        else:
                            return [float(vlr_ped_ini.value())]
                
                vlr_pedido = valor_pedido()
                
                def data():
                    if checkbox_data.isChecked():
                        if data_inicial.selectedDate() == None or data_final.selectedDate() == None:
                            QMessageBox.warning(self, "Erro", "Preencha a data inicial e final!")
                            return None
                        else:
                            return [data_inicial.selectedDate(), data_final.selectedDate()]
                    else:
                        return None
                
                dat_pedido = data()
                
                ## Regras
                
                if num_pedidos == None and nom_cliente == None and nom_operador == None and vlr_pedido == None and dat_pedido == None:
                    QMessageBox.warning(self, "Erro", "Preencha pelo menos um campo!")
                    return None
                
                if num_pedidos != None:
                    if len(num_pedidos) == 2:
                        if num_pedidos[0] == 0 or num_pedidos[1] == 0:
                            QMessageBox.warning(self, "Erro", "O numero do pedido inicial ou final não podem ser 0!")
                            return None
                        if num_pedidos[0] > num_pedidos[1]:
                            QMessageBox.warning(self, "Erro", "O numero do pedido inicial não pode ser maior que o final!")
                            return None
                        
                        
                    else:
                        if num_pedidos[0] == 0:
                            QMessageBox.warning(self, "Erro", "O numero do pedido inicial não pode ser 0!")
                            return None
                        
                if dat_pedido != None:
                    if dat_pedido[0] > dat_pedido[1]:
                        QMessageBox.warning(self, "Erro", "A data inicial não pode ser maior que a final!")
                        return None
                
                if vlr_pedido != None:
                    if len(vlr_pedido) == 2:
                        if vlr_pedido[0] == 0.00 or vlr_pedido[1] == 0.00:
                            QMessageBox.warning(self, "Erro", "O valor inicial ou final não podem ser 0!")
                            return None
                        if vlr_pedido[0] > vlr_pedido[1]:
                            QMessageBox.warning(self, "Erro", "O valor inicial não pode ser maior que o final!")
                            return None
                                            
                    else:
                        if vlr_pedido[0] == 0.00:
                            QMessageBox.warning(self, "Erro", "O valor inicial não pode ser 0!")
                            return None
                    
                ## Filtrar tabela baseando-se nos filtros
                
                # For item in tabela_pedidos
                
                for i in range(tabela_pedidos.rowCount()):
                    if num_pedidos != None:
                        if len(num_pedidos) == 2:
                            if int(tabela_pedidos.item(i, 0).text()) >= num_pedidos[0] and int(tabela_pedidos.item(i, 0).text()) <= num_pedidos[1]:
                                tabela_pedidos.setRowHidden(i, False)
                            else:
                                tabela_pedidos.setRowHidden(i, True)
                        else:
                            if int(tabela_pedidos.item(i, 0).text()) == num_pedidos[0]:
                                tabela_pedidos.setRowHidden(i, False)
                            else:
                                tabela_pedidos.setRowHidden(i, True)
                                
                    if nom_cliente != None:
                        if nom_cliente.upper() in tabela_pedidos.item(i, 3).text().upper():
                            tabela_pedidos.setRowHidden(i, False)
                        else:
                            tabela_pedidos.setRowHidden(i, True)
                            
                    if nom_operador != None:
                        if nom_operador.upper() in tabela_pedidos.item(i, 2).text().upper():
                            tabela_pedidos.setRowHidden(i, False)
                        else:
                            tabela_pedidos.setRowHidden(i, True)
                            
                    if vlr_pedido != None:
                        if len(vlr_pedido) == 2:
                            if float(tabela_pedidos.item(i, 4).text().replace("R$ ", "").replace(",", ".")) >= vlr_pedido[0] and float(tabela_pedidos.item(i, 4).text().replace("R$ ", "").replace(",", ".")) <= vlr_pedido[1]:
                                tabela_pedidos.setRowHidden(i, False)
                            else:
                                tabela_pedidos.setRowHidden(i, True)
                        else:
                            if float(tabela_pedidos.item(i, 4).text().replace("R$ ", "").replace(",", ".")) == vlr_pedido[0]:
                                tabela_pedidos.setRowHidden(i, False)
                            else:
                                tabela_pedidos.setRowHidden(i, True)
                                
                    if dat_pedido != None:
                        if dat_pedido[0] <= QDate.fromString(tabela_pedidos.item(i, 1).text(), "dd/MM/yyyy") and dat_pedido[1] >= QDate.fromString(tabela_pedidos.item(i, 1).text(), "dd/MM/yyyy"):
                            tabela_pedidos.setRowHidden(i, False)
                        else:
                            tabela_pedidos.setRowHidden(i, True)
                    
                self.ui2.close()               
           
            botao_filtro_ped_filtrar.clicked.connect(filtros)
            botao_filtro_ped_cancelar.clicked.connect(lambda: self.ui2.close())
            
        def limpar_filtros():
            for i in range(tabela_pedidos.rowCount()):
                tabela_pedidos.setRowHidden(i, False)
                
            campo_num_pedido.setText("")
            campo_cliente.setText("")
            campo_operador.setText("")
            campo_data_hora.setText("")
            campo_total_pedido.setText("")
            
            tabela_produtos_pedido.setRowCount(0)
        
        def atualizar_tabela_pedidos():
            with open("dados/pedidos.json", "r") as arquivo:
                pedidos = json.load(arquivo)
                
            tabela_pedidos.setRowCount(len(pedidos['pedidos']))
            tabela_pedidos.setColumnCount(5)
            tabela_pedidos.setHorizontalHeaderLabels(["Número do pedido", "Data e Hora", "Operador", "Cliente", "Valor total"])
            
            for i in range(len(pedidos['pedidos'])):
                for j in range(5):
                    num_ped = pedidos['pedidos'][i]['Numero do pedido']
                    data_hora = pedidos['pedidos'][i]['Data e hora']
                    operador = pedidos['pedidos'][i]['Operador']
                    cliente = pedidos['pedidos'][i]['Cliente']
                    valor_total = pedidos['pedidos'][i]['Valor total']
                
                    dados = [num_ped, data_hora, operador, cliente, valor_total]
                    
                    tabela_pedidos.setItem(i, j, QTableWidgetItem(str(dados[j])))
                    
            tabela_pedidos.setColumnWidth(0, 150)
            tabela_pedidos.setColumnWidth(1, 150)
            tabela_pedidos.setColumnWidth(2, 165)
            tabela_pedidos.setColumnWidth(3, 165)
            tabela_pedidos.setColumnWidth(4, 135)
            
            # Centralizar tudo
            for i in range(len(pedidos['pedidos'])):
                for j in range(5):
                    tabela_pedidos.item(i, j).setTextAlignment(Qt.AlignCenter)
                    
            tabela_pedidos.setEditTriggers(QTableWidget.NoEditTriggers)
            # Desativar seleção de múltiplas linhas
            tabela_pedidos.setSelectionMode(QAbstractItemView.SingleSelection)

        def atualizar_dados_pedido(codigo_pedido):
            with open("dados/pedidos.json", "r") as arquivo:
                pedidos = json.load(arquivo)
                
            for pedido in pedidos['pedidos']:
                if int(codigo_pedido) == pedido['Numero do pedido']:
                    campo_num_pedido.setText(str(pedido['Numero do pedido']))
                    campo_cliente.setText(pedido['Cliente'])
                    campo_operador.setText(pedido['Operador'])
                    campo_data_hora.setText(pedido['Data e hora'])
                    campo_total_pedido.setText(pedido['Valor total'])
                    
                    tabela_produtos_pedido.setRowCount(len(pedido['Produtos']))
                    tabela_produtos_pedido.setColumnCount(5)
                    tabela_produtos_pedido.setHorizontalHeaderLabels(["Código", "Nome", "Quantidade", "Valor unitário", "Valor total"])
                    
                    for i in range(len(pedido['Produtos'])):
                        for j in range(5):
                            tabela_produtos_pedido.setItem(i, j, QTableWidgetItem(str(pedido['Produtos'][i][list(pedido['Produtos'][i].keys())[j]])))
                            
                    tabela_produtos_pedido.resizeColumnsToContents()
                    
                    tabela_produtos_pedido.setEditTriggers(QTableWidget.NoEditTriggers)
                    
                    tabela_produtos_pedido.setColumnWidth(0, 90)
                    tabela_produtos_pedido.setColumnWidth(1, 180)
                    tabela_produtos_pedido.setColumnWidth(3, 90)
                    tabela_produtos_pedido.setColumnWidth(4, 90)
                    
                    # Centralizar tudo
                    for i in range(len(pedido['Produtos'])):
                        for j in range(5):
                            tabela_produtos_pedido.item(i, j).setTextAlignment(Qt.AlignCenter)
                            
                    break
            
        ## Configs
        
        atualizar_tabela_pedidos()
        
        ## Sinais
        
        botao_filtrar.clicked.connect(abrir_tela_filtros)
        botao_limpar_filtros.clicked.connect(limpar_filtros)
  
        tabela_pedidos.itemSelectionChanged.connect(lambda: atualizar_dados_pedido(tabela_pedidos.item(tabela_pedidos.currentRow(), 0).text()))

##############################################################################################################
    def atualizar_layout_cadastro_clientes(self):
        self.ui = self.loader.load("Layout/tela_cadastro_clientes.ui")
        self.setCentralWidget(self.ui)
        
        self.config_padrao()
        
        with open("dados/clientes.json", "r") as arquivo:
            clientes = json.load(arquivo)
        
        ## Campos
        label_clientes = self.ui.clientes_label_cadastro_clientes
        campo_codigo = self.ui.clientes_campo_codigo
        label_codigo = self.ui.clientes_label_codigo
        campo_nome_raz = self.ui.clientes_input_nomeraz
        cpf_radio = self.ui.clientes_radio_cpf
        cnpj_radio = self.ui.clientes_radio_cnpj
        label_nome_fantasia = self.ui.clientes_label_nomefan
        campo_nome_fantasia = self.ui.clientes_input_nomefan
        label_ie = self.ui.clientes_label_ie
        campo_ie = self.ui.clientes_input_ie
        label_im = self.ui.clientes_label_im
        campo_im = self.ui.clientes_input_im
        campo_cpf_cnpj = self.ui.clientes_input_cpf_cnpj
        label_endereco = self.ui.clientes_label_endereco
        campo_endereco = self.ui.clientes_input_endereco
        label_bairro = self.ui.clientes_label_bairro
        campo_bairro = self.ui.clientes_input_bairro
        label_uf = self.ui.clientes_label_uf
        campo_uf = self.ui.clientes_input_uf
        label_cidade = self.ui.clientes_label_cidade
        campo_cidade = self.ui.clientes_input_cidade
        label_cep = self.ui.clientes_label_cep
        campo_cep = self.ui.clientes_input_cep
        label_email = self.ui.clientes_label_email
        campo_email = self.ui.clientes_input_email
        label_telefone1 = self.ui.clientes_label_telefone1
        campo_telefone1 = self.ui.clientes_input_telefone1
        label_telefone2 = self.ui.clientes_label_telefone2
        campo_telefone2 = self.ui.clientes_input_telefone2
        checkbox_postergar = self.ui.clientes_chk_postergar
        
        botao_salvar = self.ui.clientes_botao_salvar
        botao_limpar = self.ui.clientes_botao_limpar
        
        ## Configs
        
        label_nome_fantasia.setVisible(False)
        campo_nome_fantasia.setVisible(False)
        label_ie.setVisible(False)
        campo_ie.setVisible(False)
        label_im.setVisible(False)
        campo_im.setVisible(False)
        
        
        campo_cpf_cnpj.setInputMask("999.999.999-99")
        campo_cep.setInputMask("99999-999")
        
        campo_telefone1.setInputMask("(99) 99999-9999")
        campo_telefone2.setInputMask("(99) 99999-9999")
        
        ## Métodos
        def mostrar_campos_cnpj(bool):
            label_nome_fantasia.setVisible(bool)
            campo_nome_fantasia.setVisible(bool)
            label_ie.setVisible(bool)
            campo_ie.setVisible(bool)
            label_im.setVisible(bool)
            campo_im.setVisible(bool)
        
        def limpar_campos():
            campo_codigo.setText("")
            campo_nome_raz.setText("")
            campo_nome_fantasia.setText("")
            campo_ie.setText("")
            campo_im.setText("")
            campo_cpf_cnpj.setText("")
            campo_endereco.setText("")
            campo_bairro.setText("")
            campo_uf.setText("")
            campo_cidade.setText("")
            campo_cep.setText("")
            campo_email.setText("")
            campo_telefone1.setText("")
            campo_telefone2.setText("")
            checkbox_postergar.setChecked(False)
        
        def consulta_cpf_cnpj(cpf_cnpj):
            with open("dados/clientes.json", "r") as arquivo:
                clientes = json.load(arquivo)
            
            lista_clientes = clientes['clientes']
            
            for cliente in lista_clientes:
                if cpf_cnpj == cliente['CPF'] or cpf_cnpj == cliente['CNPJ']:
                    QMessageBox.warning(self, "Erro", "CPF ou CNPJ já cadastrado!")
                    campo_cpf_cnpj.setText("")
                    campo_cpf_cnpj.setFocus()
                    break
            return None
        
        def ultimo_codigo_cliente():
            with open("dados/clientes.json", "r") as arquivo:
                clientes = json.load(arquivo)
            
            if clientes['clientes'] == []:
                return 1
            else:
                ultimo_cliente = max(clientes['clientes'], key=lambda x: x['Codigo do cliente'])
                ultimo_cliente = ultimo_cliente['Codigo do cliente']
                return int(ultimo_cliente) + 1
        
        def regras_clientes(self):
            
            ## Métodos de validação
            def validar_email(email):
                if email.count("@") != 1 or email.count(".") < 1:
                    return False
                else:
                    return True
            
            def validar_estados(uf):
                estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
                           "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
                           "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
                if uf.upper() in estados:
                    return True
                else:
                    return False
            
            ## Regras dos campos
            if campo_nome_raz.text() == "":
                QMessageBox.warning(self, "Erro", "Digite o nome ou razão social do cliente!")
                return False
            if len(campo_nome_raz.text()) < 4:
                QMessageBox.warning(self, "Erro", "O nome do cliente, deve ter no mínimo 4 caracteres!")
                return False
            if campo_cpf_cnpj.text() == "":
                QMessageBox.warning(self, "Erro", "Digite o CPF ou CNPJ do cliente!")
                return False
                
            if validar_email(campo_email.text()) == False:
                QMessageBox.warning(self, "Erro", "Digite um e-mail válido!")
                return False
            if validar_estados(campo_uf.text()) == False:
                QMessageBox.warning(self, "Erro", "Digite um estado válido!")
                return False
            
            
            ## Registros já cadastrados
            try:
                if campo_cpf_cnpj.text() in [cliente['CPF'] for cliente in clientes.values()]:
                    QMessageBox.warning(self, "Erro", "CPF já cadastrado!")
                    return False
                
                if campo_cpf_cnpj.text() in [cliente['CNPJ'] for cliente in clientes.values()]:
                    QMessageBox.warning(self, "Erro", "CNPJ já cadastrado!")
                    return False
                
                if campo_ie.text() in [cliente['Inscricao estadual'] for cliente in clientes.values()]:
                    QMessageBox.warning(self, "Erro", "Inscrição estadual já cadastrada!")
                    return False
                
                if campo_im.text() in [cliente['Inscricao municipal'] for cliente in clientes.values()]:
                    QMessageBox.warning(self, "Erro", "Inscrição municipal já cadastrada!")
                    return False
                
                if campo_email.text() in [cliente['E-mail'] for cliente in clientes.values()]:
                    QMessageBox.warning(self, "Aviso", "E-mail já cadastrado em outro cliente!")
                    
                if campo_telefone1.text() in [cliente['Telefone 1'] for cliente in clientes.values()]:
                    QMessageBox.warning(self, "Aviso", "Telefone já cadastrado em outro cliente!")
                
                if campo_telefone2.text() in [cliente['Telefone 2'] for cliente in clientes.values()]:
                    QMessageBox.warning(self, "Aviso", "Telefone já cadastrado em outro cliente!")
            except:
                pass
            
            return True

        def salvar_cliente(self):
            
            if regras_clientes(self) == False:
                return None
            
            cliente = {}
            cliente['Codigo do cliente'] = ultimo_codigo_cliente()
            cliente['Nome ou razao social'] = campo_nome_raz.text()
            if cpf_radio.isChecked():
                cliente['CPF'] = campo_cpf_cnpj.text()
            else:
                cliente['Nome fantasia'] = campo_nome_fantasia.text()
                cliente['CNPJ'] = campo_cpf_cnpj.text()
                cliente['Inscricao estadual'] = campo_ie.text()
                cliente['Inscricao municipal'] = campo_im.text()
            cliente['Endereco'] = campo_endereco.text()
            cliente['Bairro'] = campo_bairro.text()
            cliente['Cidade'] = campo_cidade.text()
            cliente['UF'] = campo_uf.text()
            cliente['CEP'] = campo_cep.text()
            cliente['E-mail'] = campo_email.text()
            cliente['Telefone 1'] = campo_telefone1.text()
            cliente['Telefone 2'] = campo_telefone2.text()
            cliente['Postergar'] = checkbox_postergar.isChecked()
            
            self.lista_cad_clientes.append(cliente)
            
            with open("dados/clientes.json", "r") as arquivo:
                clientes = json.load(arquivo)
            
            clientes['clientes'].append(cliente)
            
            with open("dados/clientes.json", "w") as arquivo:
                json.dump(clientes, arquivo, indent=4)
            
            
            QMessageBox.information(self, "Sucesso", f"Cliente cadastrado com sucesso! Código do cliente: {cliente['Codigo do cliente']}")
            self.atualizar_layout_cadastro_clientes()
            
        ## Sinais
        cpf_radio.clicked.connect(lambda: campo_cpf_cnpj.setInputMask("999.999.999-99"))
        cpf_radio.clicked.connect(lambda: mostrar_campos_cnpj(False))
        
        cnpj_radio.clicked.connect(lambda: campo_cpf_cnpj.setInputMask("99.999.999/9999-99"))
        cnpj_radio.clicked.connect(lambda: mostrar_campos_cnpj(True))
        
        campo_cpf_cnpj.editingFinished.connect(lambda: consulta_cpf_cnpj(campo_cpf_cnpj.text()))
        
        botao_salvar.clicked.connect(lambda: salvar_cliente(self))
        botao_limpar.clicked.connect(lambda: limpar_campos())
        
##############################################################################################################

    def atualizar_layout_nova_os(self):
        self.ui = self.loader.load("Layout/tela_cadastro_os.ui")
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Sistema de Vendas - Nova OS")
        
        self.config_padrao()
        
        self.acessorios_incluidos = []
        
        ## Campos
        campo_cliente = self.ui.os_campo_cliente
        botao_buscar_cliente = self.ui.os_buscar_cliente
        botao_cadastrar_cliente = self.ui.os_cadastrar_cliente
        
        responsavel_os = self.ui.os_responsavel
        tipo_aparelho = self.ui.os_tipo_aparelho
        botao_inserir_acessorio = self.ui.os_inserir_acessorio
        botao_remover_acessorio = self.ui.os_remover_acessorio
        acessorios = self.ui.os_acessorios_adic
        
        servico_solicitado = self.ui.os_servico_solicitado
        chk_defeito = self.ui.os_chk_defeito
        defeito_aparente = self.ui.os_defeito_aparente
        
        data_abertura = self.ui.os_data_abertura
        data_previsao = self.ui.os_data_previsao
        
        valor_previsto = self.ui.os_total_previsto
        
        
        botao_cadastrar_os = self.ui.os_cadastrar_os
        botao_cancelar = self.ui.os_cancelar
        
        ## Configs
        data_abertura.setText(data_e_hora_atuais)
        data_prevista = (datetime.now() + timedelta(days=3), "%d/%m/%Y %H:%M")
        data_prevista = data_prevista[0].strftime(data_prevista[1])
        data_previsao.setText(data_prevista)
        
        
        
        ## Métodos
        def buscar_cliente(self):
            self.ui_buscar_cliente = self.loader.load("Layout/tela_buscar_cliente.ui")
            self.ui_buscar_cliente.setModal(True)
            self.ui_buscar_cliente.setFixedSize(self.ui_buscar_cliente.size())
            self.ui_buscar_cliente.show()
            
            campo_busca = self.ui_buscar_cliente.buscar_cliente_campo
            tabela = self.ui_buscar_cliente.buscar_cliente_tabela
            
            def atualizar_tabela_clientes():
                with open("dados/clientes.json", "r") as arquivo:
                    clientes = json.load(arquivo)
                    
                tabela.setRowCount(len(clientes['clientes']))
                tabela.setColumnCount(3)
                tabela.setHorizontalHeaderLabels(["Código", "Nome ou razão social", "CPF/CNPJ"])
                
                for i in range(len(clientes['clientes'])):
                    for j in range(3):
                        tabela.setItem(i, j, QTableWidgetItem(str(clientes['clientes'][i][list(clientes['clientes'][i].keys())[j]])))
                
                # Centralizar tudo
                for i in range(len(clientes['clientes'])):
                    for j in range(3):
                        tabela.item(i, j).setTextAlignment(Qt.AlignCenter)

                tabela.setEditTriggers(QTableWidget.NoEditTriggers)
                tabela.setSelectionMode(QAbstractItemView.SingleSelection)
            
                
                def filtrar_tabela(texto):
                    for i in range(len(clientes['clientes'])):
                        codigo_cliente = str(clientes['clientes'][i]['Codigo do cliente']).upper()
                        nome_razao = str(clientes['clientes'][i]['Nome ou razao social']).upper()
                        cpf_cnpj = str(clientes['clientes'][i]['CPF/CNPJ']).upper()
                        
                        if texto.upper() in codigo_cliente or texto.upper() in nome_razao or texto.upper() in cpf_cnpj:
                            tabela.setRowHidden(i, False)
                        else:
                            tabela.setRowHidden(i, True)
                
                def selecionar_cliente():
                    codigo_cliente = tabela.item(tabela.currentRow(), 0).text()
                    nome_cliente = tabela.item(tabela.currentRow(), 1).text()
                    
                    campo_cliente.setText(f"[{codigo_cliente}] - {nome_cliente}")
                    self.ui_buscar_cliente.close()
                
                tabela.doubleClicked.connect(lambda: selecionar_cliente())
                campo_busca.textChanged.connect(lambda: filtrar_tabela(campo_busca.text()))
        
            atualizar_tabela_clientes()
        
        def definir_responsavel():
            with open("dados/operadores.json", "r") as arquivo:
                operadores = json.load(arquivo)
                operadores = operadores['operadores']
            
            for operador in operadores:
                responsavel_os.addItem(operador['Nome'])
        
        def inserir_acessorio(self):
            self.ui_inserir_acessorio = self.loader.load("Layout/tela_incluir_acessorio.ui")
            self.ui_inserir_acessorio.setFixedSize(self.ui_inserir_acessorio.size())
            self.ui_inserir_acessorio.setModal(True)
            self.ui_inserir_acessorio.show()
            
            quantidade_acessorio = self.ui_inserir_acessorio.inc_acs_qtd
            campo_acessorio = self.ui_inserir_acessorio.inc_acs_nome
            botao_inserir = self.ui_inserir_acessorio.inc_acs
            botao_cancelar = self.ui_inserir_acessorio.inc_acs_cancelar
            
            campo_acessorio.setFocus()
            
            def inserir():
                if campo_acessorio.text() == "":
                    QMessageBox.warning(self, "Erro", "Digite o acessorio!")
                    return None
                if len(campo_acessorio.text()) < 4:
                    QMessageBox.warning(self, "Erro", "O acessorio deve ter no mínimo 4 caracteres!")
                    return None
                
                acessorio = {
                    "Nome": campo_acessorio.text(),
                    "Quantidade": quantidade_acessorio.value()
                }
                
                self.acessorios_incluidos.append(acessorio)
                
                acessorios.setText(acessorios.toPlainText() + f"{acessorio['Nome']} - {acessorio['Quantidade']} unidade(s)\n")
                
                self.ui_inserir_acessorio.close()
                
            botao_inserir.clicked.connect(lambda: inserir())
            botao_cancelar.clicked.connect(lambda: self.ui_inserir_acessorio.close())
                
        def cadastrar_os(self):
            with open("dados/os.json", "r") as arquivo:
                os = json.load(arquivo)
                
            if campo_cliente.text() == "":
                QMessageBox.warning(self, "Erro", "Selecione um cliente!")
                return None
            
            if servico_solicitado.toPlainText() == "":
                QMessageBox.warning(self, "Erro", "Digite o serviço solicitado!")
                return None
            
            if chk_defeito.isChecked():
                if defeito_aparente.toPlainText() == "":
                    QMessageBox.warning(self, "Erro", "Digite o defeito aparente!")
                    return None
            
            os['os'].append({
                "Numero da OS": len(os['os']) + 1,
                "Cliente": campo_cliente.text(),
                "Responsavel": responsavel_os.currentText(),
                "Tipo de aparelho": tipo_aparelho.currentText(),
                "Acessorios adicionais": acessorios.toPlainText(),
                "Servico solicitado": servico_solicitado.toPlainText(),
                "Defeito aparente": defeito_aparente.toPlainText(),
                "Data de abertura": data_abertura.text(),
                "Data prevista": data_previsao.text(),
                "Valor previsto": valor_previsto.text()
            })
            
            with open("dados/os.json", "w") as arquivo:
                json.dump(os, arquivo, indent=4)
                
            QMessageBox.information(self, "Sucesso", "OS cadastrada com sucesso!")
            self.atualizar_layout_nova_os()
        
        def remover_acessorio(self):
            if self.acessorios_incluidos == []:
                QMessageBox.warning(self, "Erro", "Não há acessorios para remover!")
                return None
            
            self.ui_remover_acessorio = self.loader.load("Layout/tela_remover_acessorio.ui")
            self.ui_remover_acessorio.setFixedSize(self.ui_remover_acessorio.size())
            self.ui_remover_acessorio.setModal(True)
            self.ui_remover_acessorio.show()
            
            tabela_acessorios = self.ui_remover_acessorio.rmv_acs_tabela
            
            tabela_acessorios.setRowCount(len(self.acessorios_incluidos))
            tabela_acessorios.setColumnCount(2)
            tabela_acessorios.setHorizontalHeaderLabels(["Nome", "Quantidade"])
            tabela_acessorios.setEditTriggers(QTableWidget.NoEditTriggers)
            
            for i in range(len(self.acessorios_incluidos)):
                for j in range(2):
                    tabela_acessorios.setItem(i, j, QTableWidgetItem(str(self.acessorios_incluidos[i][list(self.acessorios_incluidos[i].keys())[j]])))
            
            # Centralizar tudo
            for i in range(len(self.acessorios_incluidos)):
                for j in range(2):
                    tabela_acessorios.item(i, j).setTextAlignment(Qt.AlignCenter)
            
            def duplo_clique():
                popup = QMessageBox.question(self, "Remover", "Deseja remover o acessorio?", QMessageBox.Yes | QMessageBox.No)
                
                if popup == QMessageBox.Yes:
                    self.acessorios_incluidos.pop(tabela_acessorios.currentRow())
                    tabela_acessorios.removeRow(tabela_acessorios.currentRow())
                    
                    acessorios.setText("")
                    
                    for acessorio in self.acessorios_incluidos:
                        acessorios.setText(acessorios.toPlainText() + f"{acessorio['Nome']} - {acessorio['Quantidade']} unidade(s)\n")
                    
                    self.ui_remover_acessorio.close()
                
                else:
                    return None
                
            tabela_acessorios.doubleClicked.connect(lambda: duplo_clique())
                
                
        definir_responsavel()   
        ## Sinais
        
        botao_inserir_acessorio.clicked.connect(lambda: inserir_acessorio(self))
        botao_remover_acessorio.clicked.connect(lambda: remover_acessorio(self))
        botao_cadastrar_os.clicked.connect(lambda: cadastrar_os(self))
        botao_buscar_cliente.clicked.connect(lambda: buscar_cliente(self))    
        
##############################################################################################################
    ## Funções para manipulação de dados
##############################################################################################################
    def criar_produtos_temp(self):
        with open("dados/produtos.json", "r") as arquivo:
            produtos = json.load(arquivo)
            
        with open("dados/produtos_temp.json", "w") as arquivo:
            json.dump(produtos, arquivo, indent=4)
     
    def listar_produtos_tabela(self):
        with open("dados/produtos.json", "r") as arquivo:
            produtos = json.load(arquivo)
        
        produtos = [
            [
            produto['Codigo do produto'],
            produto['Nome do produto'],
            produto['Quantidade estoque'],
            produto['Quantidade minima'],
            produto['Localizacao do produto'],
            f"R$ {produto['Valor Unitario']}".replace(".", ","),
            f"R$ {produto['Valor de aquisicao']}".replace(".", ","),
            produto['Unidade'],
            produto['Referencia'],
            produto['Observacao livre']
                
            ] for produto in produtos['produtos']
        ]
        
        for produto in produtos:
            if str(produto[2]).endswith(".0"):
                produto[2] = str(produto[2]).replace(".0", "")
            if str(produto[3]).endswith(".0"):
                produto[3] = str(produto[3]).replace(".0", "")
        
        return produtos        
    
    def limpar_pedido_temporario(self):
        with open("dados/pedido_temp.json", "w") as arquivo:
            json.dump({}, arquivo, indent=4)        
        
        
##############################################################################################################
##############################################################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    def exec():
        window.criar_produtos_temp()
        window.limpar_pedido_temporario()
        app.exec()
        
    sys.exit(exec())