/*
    Todas las funciones `add` tienen por lo menos un argumento `$parent`, que es el
    elemento en donde se va a poner la plantilla, mientras que los demás argumentos 
    dependen de qué se va a insertar. El procedimiento que siguen todas estas funciones es:

    1. Obtiene la template con base en su id.
    2. Clona la propiedad `content` de la plantilla para poder modificarla.
    3. Inserta la información correspondiente con base en los argumentos de la función.
    4. Inserta el nuevo elemento en $parent.
    5. Si aplica, reproduce una animación para que se vea bonito.

    Para ver el funcionamiento de las templates, revisar https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/template

    La función `getNewTemplate()` se encarga de obtener y procesar las templates, y
    se desglosa de la siguiente manera:

    $customTemplates.find(id) — obtiene la template con base en el id especificado.
    $($template.prop("content")) — obtiene el contenido de la template; revisar el link para más información.
    .clone(true) — crea una copia de la template, sobre la cual generaremos el nuevo elemento.
    .find(container) — por sí mismo el template clonado no se deja modificar, así que obtenemos
    el contenedor de todos los demás elementos (por etiqueta o por clase) y ahí hacemos las modificaciones.

    Adicionalmente, las instrucciones `.find()` sirven para obtener y modificar los elementos
    que están dentro del template.
*/

let $customTemplates = null;

const getNewTemplate = (id, container) =>{
    $template = $customTemplates.find(id);
    return $($template.prop("content")).clone(true).find(container);
}

const addCarouselImg = ($parent, active, picture, link) =>{
    const $carouselImgTemplate = getNewTemplate("#carouselImg-template", "div");

    if (active)
        $carouselImgTemplate.addClass("active");
    
    $carouselImgTemplate.find("img").attr("src", picture);
    $carouselImgTemplate.find("a").attr("href", link);

    $parent.append($carouselImgTemplate);
}

const addMessage = ($parent, type, message) =>{
    // Si se pone un tipo de mensaje que no sea `error`, `success` o `info`, tira una excepción.
    if (!["error", "success", "info"].includes(type)) throw new Error("addMessage() only accepts 'error', 'success' and 'info' as values for argument `type`.");

    const $msgTemplate = getNewTemplate(`#${type}Msg`, "div");

    $msgTemplate.text(message);
    $parent.append($msgTemplate);
    $msgTemplate.show('slow');
}

const addProductCard = ($parent, picture, name, price, link) =>{
    const $cardTemplate = getNewTemplate("#productCard-template", ".pcard");

    $cardTemplate.find(".pcard-img").attr("src", picture);
    $cardTemplate.find(".pcard-name").text(name);
    $cardTemplate.find(".pcard-price").text(price);
    $cardTemplate.find(".pcard-btn").attr("href", link);

    $parent.append($cardTemplate);
}

// Obtiene las templates del archivo `templates.html` y las convierte en un objeto jQuery.
let templatesReady = (async () =>{
    const response = await (await fetch("templates.html")).text();
    $customTemplates = $(new DOMParser().parseFromString(response, "text/html"));
})();