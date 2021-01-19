/* El color calculado en el vertex shader nos llega como entrada, ya interpolado para cada pixel */
varying vec4 vColor;
uniform sampler2D textura;
void main() {
    /*La unica salida de un fragment shader es el color que se va a pintar en ese pixel (gl_FragColor)
      En este caso, como la iluminacion ya la calcule en el vertex shader, me limito a pintar con el color
      que me llega interpolado
    */
    // if(vColor.r < 0.1) vColor.r = 0.0;
    // else if(vColor.r < 0.4) vColor.r = 0.4;
    // else if(vColor.r < 0.8) vColor.r = 0.8;
    // else vColor.r = 1.0;

    // gl_FragColor = vColor;

    gl_FragColor = vColor * texture2D(textura, gl_TexCoord[0].st);

}