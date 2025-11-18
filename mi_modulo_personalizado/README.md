# Gestion de Equipos

Modulo de Odoo para llevar ordenadores componentes incidencias usuarios y tags de sistemas operativos

Modelos principales
pc component con nombre tecnico especificaciones precio y moneda
pc computer con numero de equipo usuario componentes fecha de ultima modificacion precio total calculado incidencias y tags
pc os tag para guardar sistemas operativos como etiquetas

Logica y restricciones
La fecha de ultima modificacion no permite valores futuros
El precio total se calcula sumando los precios de los componentes
Los tags usan widget many2many_tags en las vistas

Seguridad
group_pc_assets_user puede leer y editar equipos y componentes
group_pc_assets_manager incluye al grupo user y puede editar todo y tags
Los permisos estan en security security xml e ir model access csv

Vistas y menus
Ordenadores tiene vista lista y formulario con componentes y tags como tags
Componentes vista lista y formulario
Sistemas Operativos vista sencilla para tags
Menu principal Equipos con accesos a cada vista

Instalacion
Copiar la carpeta odoo_addons a los addons de Odoo
Actualizar lista de apps e instalar Gestion de Equipos

Uso rapido
Crear componentes con precios
Crear tags de sistema operativo
Crear ordenadores asignando usuario componentes fecha incidencias y tags
