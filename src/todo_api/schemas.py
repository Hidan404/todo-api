from flasgger import Schema, fields

class TarefaSchema(Schema):
    id = fields.Int()
    titulo = fields.Str()
    descricao = fields.Str()
    concluida = fields.Bool()
    data_criacao = fields.DateTime()
    usuario_id = fields.Int()

class ErroSchema(Schema):
    mensagem = fields.Str()
    codigo = fields.Int()