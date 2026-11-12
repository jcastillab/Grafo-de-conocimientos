# Componentes HTML del manual

Todos tienen estilo en `plantilla.html`; no agregues CSS propio salvo que no
exista el componente. `plantilla.html` ya trae ejemplo de: índice, barra
móvil, portada (`.eyebrow`, `h1`, `.lead`), `.flow`, glosario, `.checklist` +
`.progress`, `.steps` con captura, `.note done|warn`, `.cmd`, buscador de
errores y pie. Aquí el resto.

## Avisos

```html
<div class="note tip"><b class="tag">Tip</b><p>…</p></div>
<div class="note warn"><b class="tag">Cuidado</b><p>…</p></div>
<div class="note done"><b class="tag">Listo</b><p>Cuando ves …</p></div>
<div class="note danger"><b class="tag">No</b><p>…</p></div>
```
La etiqueta puede cambiar de palabra (`Ojo`, `Tiempo`) manteniendo la clase.

## Capturas

```html
<figure class="shot"><button class="zoom" type="button" aria-label="Ampliar: ALT"><img src="img/NOMBRE.webp" alt="ALT" loading="lazy" decoding="async"></button><figcaption><b class="n">1</b> <b>Botón</b> hace X. <b class="n">2</b> …</figcaption></figure>
```
- Captura angosta (un menú lateral): `style="max-width:220px"` en el `figure`.
- Varias lado a lado: envolver en `<div class="shots">…</div>`.
- El clic abre el lightbox (ya incluido).

## Tablas

```html
<div class="tbl"><table>
  <thead><tr><th>Botón</th><th>Qué hace</th></tr></thead>
  <tbody class="num"><tr><td>…</td><td>…</td></tr></tbody>
</table></div>
```
`class="num"` en `tbody` alinea cifras (tabular-nums). La primera columna sale en negrita.

## Pasos

- `<ol class="steps steps-plain" data-list="ID">` con `<li class="step">` →
  pasos numerados 1, 2, 3 con casilla "Hecho" (`<label class="mark"><input type="checkbox" id="ID-n">Hecho</label>`) y barra `.progress` `data-progress="ID"`.
- Ruta de menú dentro de un paso: `<span class="path">Menú → Opción</span>`.

## Comandos con valores del usuario

```html
<div class="cmd"><pre data-tpl="pronostico.bat {semanas}"></pre></div>
```
`{finca}` y `{semanas}` se rellenan desde inputs `#fFinca` / `#fSemanas` si
existen en la página (ficha). Sin ficha, usa `<pre>` normal. Todo `.cmd`
tiene botón **Copiar** automático.

## Calculadora

```html
<div class="tool">
  <h3>¿Cuánto X necesito?</h3>
  <div class="row"><label class="field" for="nItems">Número de …
    <input id="nItems" type="number" min="1" step="1" value="70" inputmode="numeric"></label></div>
  <div class="result" aria-live="polite">
    <div><b id="outA">—</b><span>Etiqueta</span></div>
  </div>
  <p class="fine">De dónde salen los números.</p>
</div>
<script>
(function(){ var n=document.getElementById("nItems"); if(!n) return;
  var calc=function(){ var v=Math.max(0, parseInt(n.value,10)||0);
    document.getElementById("outA").textContent = Math.ceil(v*0.175) + " GB"; };
  n.addEventListener("input", calc); calc(); })();
</script>
```

## Trampas silenciosas (admin)

```html
<ol class="traps"><li><p><b>Título.</b> Qué pasa sin dar error y cómo detectarlo.</p></li></ol>
```

## Anexo plegable

```html
<details class="annex"><summary>Variables de entorno</summary><div>…</div></details>
```

## Otros

- Teclas: `<kbd>Ctrl</kbd> + <kbd>C</kbd>`.
- Etiqueta de versión: `<span class="ver">v2</span>`.
- Sección: `<section id="slug"><p class="eyebrow">Sección N · cuándo</p><h2>…</h2>…</section>`
  y su `<li><a data-n="N" href="#slug">…</a></li>` en el índice.
