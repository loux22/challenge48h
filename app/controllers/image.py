from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Tag, Image, Category
import os
from werkzeug.utils import secure_filename
from PIL import Image as Picture



image = Blueprint('image', __name__, url_prefix='/')


@image.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('image.importImg'))

@image.route('/import', methods=['GET', 'POST'])
def importImg():
    message_error = ""
    
    # recupére tout les tags
    tags = Tag.query.all()
    images = Image.query.all()

    if request.method == 'POST':
        typeImg = request.form.get('typeImg')
        isProduct = request.form.get('isProduct')
        isHuman = request.form.get('isHuman')
        isInstitutional = request.form.get('isInstitutional')
        credit = request.form.get('credit')
        rightOfUse = request.form.get('rightOfUse')
        copyrightImg = request.form.get('copyrightImg')
        endOfUse = request.form.get('endOfUse')
        category = request.form.get('category')
        filenames = request.files.getlist('filename')
        tagsChecked = request.form.getlist('tag')

        if isProduct == "oui" :
            isProduct = True
        else : 
            isProduct = False

        if isHuman == "oui" :
            isHuman = True
        else : 
            isHuman = False

        if isInstitutional == "oui" :
            isInstitutional = True
        else : 
            isInstitutional = False

        if rightOfUse == "oui" :
            rightOfUse = True
        else : 
            rightOfUse = False

        count_filename = 0
        for filename in filenames : 
            message_error = ""
            resp = uploadImage(filename)
            if not resp : 
                message_error = "Le type du fichier n'est pas sous le bon format"
            else :
                filenamefinal = str(filename.filename).replace(" ", "_").replace("é", "e").replace("è", "e").replace("à", "a").replace("â", "a").replace("ä", "a").replace("ê", "e").replace("ï", "i").replace("î", "i").replace("ñ", "n").replace("ô", "o").replace("ù", "u").replace(",", "_")

                for img in images :
                    if img.name == filenamefinal:
                        message_error = "cette image existe déjà dans la base de données"
                        count_filename += 1

                if message_error != "cette image existe déjà dans la base de données" :
                    formatImg = get_format_image(filenamefinal)

                    categoryImg = Category.query.filter_by(name=category).first()

                    image = Image(filenamefinal, typeImg, isProduct, isHuman, isInstitutional, formatImg , credit, rightOfUse, copyrightImg, endOfUse, categoryImg)
                    # db.session.add(image)

                    for tag in tagsChecked :
                        tagImg = Tag.query.filter_by(id=tag).first()

                        image.tags.append(tagImg)
                        db.session.add(image)
                    
                    db.session.commit()

        if len(filenames) == 1 :
            message_error = str(len(filenames) - count_filename) + " image a été ajouté et " + str(count_filename) + " existait déjà"
        else :   
            if count_filename == 1 :
                message_error = str(len(filenames) - count_filename) + " images ont été ajouté et " + str(count_filename) + " existait déjà sur les " + str(len(filenames)) + " images"
            else :  
                message_error = str(len(filenames) - count_filename) + " images ont été ajouté et " + str(count_filename) + " existaient déjà sur les " + str(len(filenames)) + " images"
        
        

    return render_template('pages/import.html', tags=tags,  message_error= message_error)




@image.route('/find', methods=['GET', 'POST'])
def findImg():
    tags = Tag.query.all()

    return render_template('pages/find.html', tags=tags)
















def get_format_image(filename):
    """ Fonction qui recupere le format de l'image (horizontal ou vertical)

    Args:
        filename [string] : nom de l'image
    
    Return [string] : horizontal ou vertical
    """
    imagename = "app/static/img/" + str(filename)
    image = Picture.open(imagename)

    width,height=image.size  

    if width >= height :
        return "horizontal"
    return "vertical"

def allowed_image(filename):
    """ Fonction qui permet de verifier si l'extension de l'image est bonne

    Args:
        filename [string] : nom de l'image
    
    Return [Boolean]
    """

    # Nous voulons uniquement des fichiers avec un. dans le nom de fichier
    if not "." in filename:
        return False

    # Séparez l'extension du nom de fichier
    ext = filename.rsplit(".", 1)[1]

    # Vérifiez si l'extension est dans ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in ["JPEG", "JPG", "PNG"]:
        return True
    else:
        return False




def uploadImage(image):
    """ Fonction qui upload une image dans le bon dossier 

    Args:
        image [request.files] : image
    
    Return [Boolean]
    """
    if allowed_image(image.filename):
        if image.mimetype == 'image/png' or image.mimetype == 'image/jpg' or image.mimetype == 'image/jpeg':

            filename = secure_filename(image.filename)
            uploads_dir = 'app/static/img/'
            os.makedirs(uploads_dir, exist_ok=True)
            image.save(os.path.join(uploads_dir, filename))

            return True

    return False



