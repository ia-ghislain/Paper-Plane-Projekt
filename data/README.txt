Hi, You !
=========

<div class="alert alert-info" role="alert">
  <span class="glyphicon glyphicon-info-sign" aria-hidden="true"></span>
  Le fichier, use *[web_struct.js][3]* permet de configurer le site web en **entier**
</div>


Utilisation
-----------

_Pour utiliser le site, modifiez web_struct.js_
```javascript
/* Json file to make the website (unipage) structure */
var struc =  {
				"site_name":"Mon super site web",
				"code_color":"Le theme voulue sans .css", //Voir fichiers dans includes/css/syntax_highlighter
				"home_title":"ISN" // Titre en en tête (écris en gros)
			 };
```
_Modifions maintenant le **menu**_
```javascript
var menu = 	 [
                {name:"Introduction",location:"README.md"}, // Nom & location d'une page (la première)
				{name:"Qui sommes nous ?",location:"WHO.md"}, // Nom & location de la seconde page
				{...} // Ne pas oublier la virgule
			 ];
```
Ajout d'images
--------------
```html
<center>![alt text][1]</center> <!-- Ou -->
<center>![alt text](/path/img.jpg "Title")</center>
```
Resultats : 
<center>![alt text][1]</center>


Balises utiles
--------------
```html
<span class="glyphicon glyphicon-info-sign"> Une information </span>
```
Rendu : <span class="glyphicon glyphicon-info-sign"> Une information </span>
```html
<span class="glyphicon glyphicon-warning-sign"> Un avertissement </span>
```
Rendu : <span class="glyphicon glyphicon-warning-sign"> Un avertissement </span> 
```html
<div class="alert alert-warning" role="alert">
	<span class="glyphicon glyphicon-warning-sign" aria-hidden="true"></span>
	Une alerte
</div>
```
Rendu : <div class="alert alert-warning" role="alert">
	<span class="glyphicon glyphicon-warning-sign" aria-hidden="true"></span>
	Une alerte
</div>

<div class="alert alert-info" role="alert">
  <span class="glyphicon glyphicon-info-sign" aria-hidden="true"></span>
  Vous pouvez utiliser *[Cette editeur][4]* pour gérérer des pages
</div>

[1]: http://placehold.it/350x150
[2]: http://daringfireball.net/projects/markdown/
[3]: includes/js/web_struct.js
[4]: http://daringfireball.net/projects/markdown/dingus