from sqlalchemy.orm import Session
from api.models.usuario import Usuario


class UsuarioRepository:

    def __init__(self, db: Session):
        self.db = db

    
    def buscar_por_email(self, email: str):
        
        return (
            self.db.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )


    def buscar_por_id(self, usuario_id: int):

        return (
            self.db.query(Usuario)
            .filter(Usuario.id == usuario_id)
            .first()
        )

    def listar(self):
        return (
            self.db.query(Usuario)
            .all()
        )

    def criar(self, nome: str, email: str, senha: str):
        
        usuario = Usuario(
            nome = nome,
            email = email,
            senha = senha
        )

        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)

        return usuario

    def atualizar(self, usuario: Usuario, nome: str, email: str, senha: str):

        usuario.nome = nome
        usuario.email = email
        usuario.senha = senha
        
        self.db.commit()
        self.db.refresh(usuario)

        return usuario

    def deletar(self, usuario: Usuario):
        self.db.delete(usuario)
        self.db.commit()