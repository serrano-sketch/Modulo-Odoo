Gestion de Equipos - Documentacion

Descripcion general:
Aplicacion desarrollada para Odoo 18 que lleva el inventario de ordenadores corporativos, sus componentes, incidencias, usuarios y sistemas operativos instalados. Se instala como módulo independiente dentro de la carpeta extra-addons.

Modelos incluidos:
pc.component almacena el nombre tecnico, las especificaciones, el precio monetario y la moneda de referencia para cada componente reutilizable.
pc.computer representa cada equipo con numero de inventario, usuario asignado (Many2one a res.users), lista de componentes (Many2many a pc.component), fecha de ultima modificacion, incidencias, precio total calculado y etiquetas de sistema operativo.
pc.os.tag sirve como catalogo libre de sistemas operativos que se asignan a los equipos mediante Many2many.
mi_modulo_personalizado.registro permite registrar notas generales y actividades del modulo en un menu independiente.

Logica y restricciones:
El campo last_mod_date del modelo pc.computer se valida mediante _check_last_mod_date para impedir fechas futuras; en caso de incumplimiento se lanza ValidationError.
El campo price_total se calcula automaticamente con _compute_total sumando los precios de los componentes relacionados y respetando la moneda definida en currency_id.
Los campos monetarios usan la moneda de la compania (env.company.currency_id) para garantizar consistencia.

Seguridad y grupos:
El archivo security/security.xml define dos grupos: group_pc_assets_user para usuarios internos con permisos de lectura y edicion basica, y group_pc_assets_manager con acceso completo e implicacion del grupo anterior.
Los permisos de acceso se declaran en security/ir.model.access.csv otorgando crear, leer, escribir y eliminar segun el grupo.

Vistas y menus:
Cada modelo dispone de vistas list y form en la carpeta views. El modulo crea el menu principal Equipos con accesos a Ordenadores, Componentes y Sistemas Operativos. El modelo de registro cuenta con su propio menu raiz llamado Registros del modulo para que pueda consultarse de forma independiente. Los campos Many2many en pc.computer utilizan el widget many2many_tags para facilitar la seleccion rapida de componentes y sistemas operativos.

Instalacion y actualizacion:
1. Copiar la carpeta mi_modulo_personalizado dentro de /mnt/extra-addons o la ruta equivalente del servidor.
2. Reiniciar el servicio de Odoo y actualizar la lista de aplicaciones.
3. Instalar Gestion de Equipos desde el modulo de Apps o actualizarla con el comando odoo -u mi_modulo_personalizado -d <basedatos>.

Uso recomendado:
1. Crear los componentes reutilizables con sus precios y especificaciones.
2. Registrar los sistemas operativos que se usan en la empresa como etiquetas.
3. Dar de alta cada ordenador asignando usuario, componentes, tags y registrando incidencias o intervenciones.
4. Registrar notas generales en el menu Registros cuando sea necesario dejar evidencia adicional.

Notas finales:
El modulo no incluye datos demo ni traducciones por defecto. Si se requiere otro idioma, anadir ficheros PO correspondientes. Para desplegarlo en otra instancia repetir el proceso de instalacion y ejecutar la actualizacion con la base de datos destino. Para documentacion adicional revisar los comentarios en los modelos dentro de la carpeta models.
