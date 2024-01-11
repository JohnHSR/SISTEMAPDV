from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QMessageBox, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
import sys, json,datetime



versao = "1.0"
data_e_hora_atuais = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
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
            
    def atualizar_hora(self):
        data_e_hora_atuais = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
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
                            registro['Quantidade em estoque'] = int(registro['Quantidade em estoque']) - int(quantidade)
                        else:
                            registro['Quantidade em estoque'] = float(registro['Quantidade em estoque']) - float(quantidade)
                            
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
                    
                    <h2 style="text-align:center"><strong>==============================</strong></h2>
                    
                    <p>&nbsp;</p>
                    
                """  
                cupom_pedido.append(produto)
                
                self.pedido['Numero do pedido'] = ''
                self.pedido['Data e hora'] = ''
                self.pedido['Operador'] = ''
                self.pedido['Cliente'] = ''
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
                
                if pedidos == {} or pedidos is None:
                    return 1
                
                ultimo_pedido = max(pedidos.keys())
                ultimo_pedido = int(ultimo_pedido) + 1
                
                return ultimo_pedido
            
            def baixar_produtos_estoque(codigo):
                with open("dados/pedido_temp.json", "r") as arquivo:
                    pedido_temp = json.load(arquivo)
                
                with open("dados/produtos.json", "r") as arquivo:
                    produtos = json.load(arquivo)
                
                for produto in pedido_temp['Produtos']:
                    for registro in produtos['produtos']:
                        if produto['Codigo do produto'] == registro['Codigo do produto']:
                            if str(registro['Quantidade em estoque']).endswith(".0") and str(produto['Quantidade']).endswith(".0"):
                                registro['Quantidade em estoque'] = int(registro['Quantidade em estoque']) - int(produto['Quantidade'])
                            else:
                                registro['Quantidade em estoque'] = float(registro['Quantidade em estoque']) - float(produto['Quantidade'])
                                
                
                with open ("dados/produtos.json", "w") as arquivo:
                    json.dump(produtos, arquivo, indent=4)
                
            def finalizar_pedido():
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
                            
                        pedidos[self.pedido['Numero do pedido']] = self.pedido
                        
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
                        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><style type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;">\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">-------------------------------------------------------------------------------------------------</span></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;"><br /></p>\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">SISTEMA DE VENDAS</span></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;"><br /></p>\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Razão Social da empresa</span></p>\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">CNPJ: 00.000.000/0001-00</span></p>\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">John H. (77) 90000-0000</span></p>\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">Av. João Bobo Nº 000</span></p>\n<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;"><br /></p>\n<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">----------------------------------------------------------------------------------------------</span></p></body></html>
                        """
                        
                        cupom_pedido.setText(cupom)
                
                        
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
            
        ## Configs
        
        ## Sinais
        
        input_codigo_produto.textChanged.connect(lambda: Produto.atualizar_dados_produto(input_codigo_produto.text()))
        input_quantidade_produto.valueChanged.connect(lambda: Produto.atualizar_dados_produto(input_codigo_produto.text()))
        
        botao_adicionar_produto.clicked.connect(lambda: Produto.adicionar_produto_cupom())
        
        campo_valor_desconto.valueChanged.connect(lambda: Produto.somar_total_pedido())
        campo_porc_desconto.valueChanged.connect(lambda: Produto.somar_total_pedido())
        
        campo_valor_adicional.valueChanged.connect(lambda: Produto.somar_total_pedido())
        campo_porc_adicional.valueChanged.connect(lambda: Produto.somar_total_pedido())         
        
        
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
                pass
            
            
            botao_filtro_ped_cancelar.clicked.connect(lambda: self.ui2.close())
            ## Configs
        
        ## Configs
        
        ## Sinais
        
        botao_filtrar.clicked.connect(abrir_tela_filtros)

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
        cpf_radio.clicked.connect(lambda: campo_cpf_cnpj.setInputMask("99.999.999-99"))
        cpf_radio.clicked.connect(lambda: mostrar_campos_cnpj(False))
        
        cnpj_radio.clicked.connect(lambda: campo_cpf_cnpj.setInputMask("99.999.999/9999-99"))
        cnpj_radio.clicked.connect(lambda: mostrar_campos_cnpj(True))
        
        campo_cpf_cnpj.editingFinished.connect(lambda: consulta_cpf_cnpj(campo_cpf_cnpj.text()))
        
        botao_salvar.clicked.connect(lambda: salvar_cliente(self))
        botao_limpar.clicked.connect(lambda: limpar_campos())
        
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
            produto['Quantidade em estoque'],
            produto['Quantidade minima'],
            produto['Localizacao do produto'],
            f"R$ {produto['Valor Unitario']}".replace(".", ","),
            f"R$ {produto['Valor de aquisicao']}".replace(".", ","),
            produto['Unidade'],
            produto['Referencia'],
            produto['Observacao livre']
                
            ] for produto in produtos['produtos']
        ]
        
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