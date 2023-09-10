from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
           
        }
class Usuario(db.Model):
    __tablename__ = 'usuario'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String(250), nullable=False,unique=False)  
    email = db.Column(db.String(250),nullable=False,unique=True)
    password = db.Column(db.String(450), nullable=False,unique=False)
    favoritos = db.relationship("Favoritos",back_populates="usuario")

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name

    def __repr__(self):
        return f'<Usuarios {self.email} {self.password} {self.name}>'

    def serialize(self):
        favoritos=[fav.serialize() for fav in self.favoritos]
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "favoritos":favoritos
           
        }
  
    def delete_and_commit(self):
        """
            Elimina la instancia a la sesión (delete) y salva los cambios en la base de datos (commit).
            Si algo sale mal en este proceso, lo deshace (rollback) y retorna False.
            Si todo sale bien, retorna True
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as error:
            print("Error del tipo", type(error))
            print("Error: ", error)
            print("Error args: ", error.args)
            db.session.rollback()
            return False

class Personajes(db.Model):
    __tablename__ = 'personajes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    person_class = db.Column(db.String(250), nullable=True)
    faccion = db.Column(db.String(250), nullable=True)
    race = db.Column(db.String(250), nullable=True)
    gender =db.Column(db.String(250), nullable=True)
    favoritos = db.relationship("Favoritos",back_populates="personajes")
    

    def __init__(self,**kwargs):
        self.name =  kwargs["name"]
        self.faccion = kwargs["faccion"]
        self.person_class=  kwargs["person_class"]
        self.race =  kwargs["race"]
        self.gender =  kwargs["gender"]

    def __repr__(self):
        return f'<personajes {self.faccion} {self.person_class} {self.name} {self.race} {self.gender}>'

    def serialize(self):
        return {
            "id": self.id,
            "faccion": self.faccion,
            "person_class": self.person_class,
            "race":self.race,
            "gender":self.gender,
            "name":self.name

            
        }

  
class Planetas(db.Model):    
    __tablename__ = 'planetas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable= True)
    size = db.Column(db.String(250), nullable= True)
    temp =  db.Column(db.Integer, nullable= True)
    color = db.Column(db.String(250), nullable= True)
    moon_numbers = db.Column(db.String(250), nullable= True)
    favoritos=db.relationship("Favoritos",back_populates="planetas")

    
    def __init__(self,**kwargs):
        self.name =  kwargs["name"]
        self.size = kwargs["size"]
        self.temp =  kwargs["temp"]
        self.color =  kwargs["color"]
        self.moon_numbers =  kwargs["moon_numbers"]

    def __repr__(self):
        return f'<planetas {self.size} {self.temp} {self.color} {self.moon_numbers} {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "size": self.size,
            "temp": self.temp,
            "color":self.color,
            "moon_numbers":self.moon_numbers,
            "name":self.name   

            
        }

        


class Favoritos(db.Model):
    __tablename__ = 'favoritos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('usuario.id'), nullable=True)
    usuario=db.relationship("Usuario",back_populates="favoritos")  
    personaje_id = db.Column(db.ForeignKey('personajes.id'), nullable=True)
    personajes=db.relationship("Personajes",back_populates="favoritos") 
    planet_id = db.Column(db.ForeignKey('planetas.id'), nullable=True)
    planetas=db.relationship("Planetas",back_populates="favoritos") 

    def serialize(self) :
      
        return {

            "id": self.id,
            "user_id":self.user_id,
            "personaje_id":self.personaje_id,       
            "planet_id": self.planet_id,
            

            #"planeta": self.planetas.serialize(),

            #"personaje": self.personajes.serialize()
        }

    # def serializeplaneta(self):
    #     return {

    #     "planeta": self.planetas.serialize()
    #     }
    def delete(self):
        """
            Elimina la instancia a la sesión (delete) y salva los cambios en la base de datos (commit).
            Si algo sale mal en este proceso, lo deshace (rollback) y retorna False.
            Si todo sale bien, retorna True
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as error:
            print("Error del tipo", type(error))
            print("Error: ", error)
            print("Error args: ", error.args)
            db.session.rollback()
            return False        