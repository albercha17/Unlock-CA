# Ideas de puzles y juegos que usan el móvil (23 oct 2026)

Lluvia de ideas para sacar partido a los sensores del móvil en nuestros juegos (que son una web instalable). Primero, qué se puede y qué no; después, ideas de puzles sueltos para meter en los juegos actuales y, al final, juegos nuevos pensados desde el móvil. Todo lo marcado con **[Android]** no funciona en iPhone y necesita una alternativa táctil (regla de la serie: nunca un sensor como única vía).

> **Decisión (23 oct 2026): el móvil es un iPhone.** Se descartan las ideas que solo funcionan en Android: vibración, linterna encendida por la app, NFC y batería. Lo que sí vale en iPhone (Safari o la app instalada): micrófono, cámara, acelerómetro y giroscopio (con botón de permiso), brújula, `visibilitychange`, Wake Lock (iOS 16.4 o superior), multitoque y sonido. El reconocimiento de voz es poco fiable: solo como extra, con teclado de respaldo. En iPhone el sonido y el micrófono solo arrancan tras un toque del jugador, y el interruptor de silencio apaga el sonido de la web (lo que da el truco de «tono + micro» para comprobarlo).
> Ideas que quedan descartadas por esto: 12 (linterna del compañero con vibración), la vibración como señal en cualquier puzle y todo lo marcado **[Android]**. La «luz» de la partida será siempre la pantalla en blanco.

## 1. Qué se puede hacer desde una web

| Sensor / acción | ¿Se puede? | Cómo y trampas |
|---|---|---|
| **Micrófono** | Sí | `getUserMedia` + `AnalyserNode`: volumen, silencio, soplar, aplaudir, silbar (tono), contar palmadas. Pide permiso; solo con HTTPS (GitHub Pages lo es). |
| **Cámara** | Sí | `getUserMedia`: luz/oscuridad (tapar la cámara con el dedo), color medio de lo que enfoca (apuntar a algo rojo), detectar movimiento, leer un dibujo impreso (comparando contra una plantilla). Sin QR (decisión del 17 oct). |
| **Linterna encendida por la app** | **[Android]** | Pedir `torch` a la pista de la cámara trasera. En iPhone no existe. Alternativa: pantalla blanca a máximo brillo como «luz». |
| **Detectar que el usuario enciende su linterna** | Sí, con la cámara | Medir la luz que entra por la cámara: si sube de golpe, hay una linterna delante (por ejemplo, iluminar una carta con ventana a través del móvil). |
| **Agitar / golpear / inclinar** | Sí | `DeviceMotionEvent` (acelerómetro) y `DeviceOrientationEvent` (giroscopio/brújula). En iPhone hay que pedir permiso con un botón. |
| **Brújula (hacia dónde apunta el móvil)** | Sí (más fiable en Android) | `deviceorientationabsolute`. Útil para «apunta al norte». Calibrar y dejar tolerancia amplia. |
| **Vibración** | **[Android]** | `navigator.vibrate`. Nunca como única señal: acompañar de luz y sonido. |
| **Subir/bajar el brillo del sistema** | **No** | Una web no puede leerlo ni cambiarlo. **Truco:** medir el brillo *efectivo* con la cámara frontal o pedirle al jugador que «tape la pantalla» y medir oscuridad; o hacer que la propia pantalla de la app pase de negra a blanca (nuestro brillo) y que el jugador la use de linterna. |
| **Detectar el modo silencio / volumen** | **No directamente** | **Truco:** la app emite un tono y el micrófono comprueba si lo oye. Si no lo oye, el móvil está silenciado (o hay ruido de fondo: dar margen). Así «mutea el móvil» o «sube el volumen al máximo» sí se puede comprobar. |
| **Cambio de app / pantalla apagada** | Sí | `visibilitychange`: la app sabe cuándo el jugador se va y vuelve (sirve para «mira otra cosa y vuelve»). `Wake Lock` evita que se apague la pantalla durante un puzle. |
| **Giro de pantalla (vertical/horizontal)** | Sí | `screen.orientation` y `matchMedia`. |
| **Multitoque** | Sí | Varios dedos a la vez (ya usado en el teléfono rojo del Espía). Dos jugadores: dos dedos de cada uno en la misma pantalla. |
| **Sonido** | Sí | Web Audio: tonos, ritmos, melodías, sonido en estéreo (con auriculares: «de qué lado viene»). Ya lo usamos en el morse y en la radio. |
| **Voz (reconocimiento)** | Parcial | `SpeechRecognition` funciona bien en Chrome/Android y regular en iPhone; necesita internet. Úsese para «di la contraseña», con teclado como respaldo. |
| **Batería, red, hora** | Parcial | `navigator.onLine` (modo avión: «corta la comunicación»), hora y fecha del móvil (puzles de «solo se abre a las 3:15»), batería **[Android]**. |
| **Ubicación (GPS)** | Sí, pero poco útil en casa | Solo para juegos «de calle». |
| **NFC / Bluetooth** | **[Android]** | Web NFC permite leer etiquetas. Interesante para cartas con pegatina NFC, pero excluye iPhone: solo como extra. |
| **Cámara frontal + cara** | Posible | Detectar «cara presente» o sonrisa es pesado y cuestiona la privacidad; mejor evitarlo. |

**Reglas para todos:** pedir cada permiso solo cuando el puzle lo necesita; botón de «no puedo / no tengo permiso» que ofrece una versión táctil equivalente; margen de tolerancia amplio; el sensor nunca es la única forma de avanzar; y los datos (audio, vídeo) no salen del móvil.

## 2. Puzles sueltos (para meter en los juegos que ya hay)

Cada uno dice el sensor, la idea, y en qué ambientación encaja. Todos llevan una versión táctil de respaldo.

### Micrófono
1. **Soplar la vela / el polvo** (Cuento, Egipto, Pompeya): hay que soplar al micro para apagar velas **en el orden** que dice una carta; cada soplo apaga la más cercana al volumen detectado (suave = vela pequeña, fuerte = grande).
2. **Silencio absoluto** (Espía, Faro, Juguetes): «los juguetes se despiertan»: hay que mantener el silencio 10 s mientras un indicador sube con el ruido. Un compañero tiene que hacer algo (pasar una carta) sin hacer ruido.
3. **Contar palmadas** (Egipto, Oeste, Fútbol): la carta dice «tantas palmadas como…» y la app las cuenta (ritmo: lenta/rápida). Fútbol: la grada.
4. **Silbar la nota** (Oeste, Cuento, Piratas): la app oye un tono que silbas y lo compara con una nota de la carta (afinar «a oído» con una barra).
5. **Eco/sonar** (Piratas, Marte): la app emite un tono y el micro mide el «eco» en un espacio (taparlo con la mano). Más abstracto: adivina si el móvil está en un cajón (sonido amortiguado).
6. **Ritmo de la carta** (Arcade, Juguetes): una partitura dibujada en una carta y hay que golpear la mesa con el ritmo (el micro detecta golpes).
7. **«¿Está sonando mi móvil?»** (todos): puzle de comprobar que el sonido del móvil está activo (ver el truco del silencio): la historia pide «poner el volumen al máximo» o «ponerlo en silencio».

### Cámara
8. **Tapar el objetivo** (Faro, Dinosaurios, Marte): «la oscuridad de la cueva»: tapar la cámara con el dedo hace aparecer unas marcas luminosas en la pantalla (la app muestra pistas solo en oscuridad). Respaldo: botón «apagar luz».
9. **Linterna sobre la carta** (Egipto, Pompeya, Espía): la carta lleva escrito en tinta clara (o pintada con un patrón) algo que solo se lee con la cámara con luz fuerte. Ojo: más difícil de imprimir bien.
10. **Apuntar a un color** (Florencia, Oeste, Cuento): «busca en la carta el color del tinte»: la app comprueba que la cámara apunta a un color (rojo, azul…) y avanza. Fuente de color: la propia carta o un objeto de la casa.
11. **Cámara como detector de movimiento** (Espía, Fútbol): «sigilo»: hay que mover un objeto delante de la cámara sin que la app detecte movimiento brusco.
12. **Luz del jugador** (Faro, Piratas, Juguetes): encender la linterna del móvil de un compañero hacia la cámara de otro dispositivo: la app mide la luz y desbloquea. Dos móviles: uno emite y otro mide. Con un solo móvil: el brillo de la pantalla en blanco sirve de luz.

### Acelerómetro / giroscopio
13. **Agitar** (Piratas, Oeste, Juguetes): «agita el cóctel / la lata de pintura / el cubo de dados» N veces, con una intensidad (suave = mezcla, fuerte = revienta). Respaldo: pulsar el botón N veces.
14. **Nivel de burbuja** (Faro, Egipto, Florencia): mantener el móvil plano para equilibrar una balanza, el astrolabio o el agua de un cuenco. Tolerancia amplia.
15. **Brújula** (Faro, Piratas, Marte): «orientar» la antena, el astrolabio o la brújula hacia un rumbo que dan las cartas; vibra/pita al acercarse.
16. **Golpecitos en la mesa** (Espía, Trono, Arcade): código Morse con golpes en la mesa (el acelerómetro los detecta, sin micro).
17. **Dar la vuelta al móvil** (Dinosaurios, Cuento, Juguetes): «vuelca la lámpara / la caja»: el móvil boca abajo es un efecto (ver la carta del reverso, vaciar un cubo).
18. **Inclinar para rodar una bola** (Arcade, Marte, Pompeya): laberinto de inclinación con una regla dibujada en una carta (ya hay algo parecido en canicas, pero con el giroscopio).

### Pantalla, brillo, linterna
19. **Pantalla blanca = luz** (Faro, Dinosaurios, Marte): la pantalla pasa a blanco puro, y se usa como lámpara sobre una carta de tinta que reacciona al color (blanco/azul/rojo). Alternar entre los tres colores de pantalla como si fueran «filtros».
20. **Mucho brillo / poco brillo** (todos): el juego no puede leer el brillo, pero sí pedir que el jugador «baje el brillo hasta que se vea la marca tenue» (una imagen con detalle en gris casi negro: si se ve, el brillo es el adecuado) o «súbelo hasta que se vea el borde». Es un puzle de percepción, no un sensor.
21. **Pantalla de linterna con color** (Piratas, Egipto): colores de pantalla (rojo, verde, azul) que «iluminan» cartas dibujadas en tinta de color: con luz roja, la tinta roja desaparece (efecto clásico de las gafas 3D rojo/azul).

### Otros
22. **Modo avión / sin red** (Espía, Marte): «cortad las comunicaciones»: la app detecta que está sin conexión y avanza; si vuelve la red, el puzle se rompe (una dificultad ingeniosa).
23. **Mirar la hora del móvil** (Pompeya, Faro, Egipto): «solo el reloj de arena dice cuándo»; la app usa la hora real: hay que dejar pasar X minutos antes de mirar o aprovechar que los minutos del reloj coinciden con la solución (por ejemplo, un código de hora y minutos).
24. **Cambiar de app / mirar otra cosa** (Espía, Fútbol): «consulta la hoja de reglas» y vuelve: la app mide cuánto tiempo estuviste fuera (útil como «ir a por una carta» y volver a la partida).
25. **Voz como contraseña** (Espía, Oeste, Trono): decir una frase de pase en voz alta, con teclado como respaldo; ofrece variaciones con sinónimos para que no importe la pronunciación.
26. **Dos móviles a la vez** (Cristina y Alberto, cada uno con su móvil): un puzle que necesita las dos pantallas: uno ve unos símbolos y el otro una tabla; o uno sostiene un botón mientras el otro hace una combinación (ya está en la lista de ideas de co-op).

## 3. Juegos nuevos pensados desde el móvil

Ideas de juegos completos cuyo núcleo es el móvil. Cada uno sigue siendo un escape room con cartas, pero el móvil es protagonista.

1. **«Frecuencia perdida»** (radio, años 60): el móvil es una radio. Girar el móvil (brújula) para buscar la dirección de una señal, el micro para oír un tono cuando estás en la buena dirección, el modo avión para cortar la emisión enemiga, el brillo para dejar la pantalla «a oscuras» mientras se escucha. Cartas: mapas con rumbos y tablas de códigos.
2. **«La noche del museo»** (sigilo): con el micrófono, hay que avanzar sin hacer ruido (silencio); con la cámara tapada, esconderse del guardia; con la linterna, buscar cosas en una carta oscura. Cartas con ventanas que se alumbran.
3. **«El laboratorio del alquimista»**: agitar para mezclar (intensidad), inclinar para verter con precisión, soplar para avivar el fuego, silbar para afinar el alambique, tapar la cámara para «cerrar el horno». Cartas con recetas en símbolos.
4. **«Fantasmas»** (casa encantada): el móvil es un detector (EMF): se mueve para buscar, vibra con cercanía; el micrófono oye «susurros» que hay que contestar; la cámara trasera enseña «fantasmas» de color en una carta con luz especial; apagar la linterna al final. Mucho ambiente.
5. **«Cuarto de baño sin luz»** (supervivencia): el móvil es la única luz de la partida; el brillo es una *moneda*: cada puzle consume «batería» (la app mide el tiempo con la pantalla blanca) y hay que gastar poco brillo con las cartas ya vistas. Es un juego de gestión con un reloj de luz.
6. **«El mensajero»** (co-op con dos móviles): cada jugador tiene un móvil con una parte del mensaje (uno oye, el otro ve); tienen que comunicarse en voz alta sin enseñarse la pantalla, con un ritmo común (palmas) para sincronizar, y una carta que describe sus pantallas por separado.
7. **«Códigos en el aire»**: todo se resuelve con sonido: la app emite tonos (DTMF), melodías y morse; el jugador silba, aplaude o canta de vuelta; las cartas tienen partituras, tablas de frecuencias y ritmos dibujados. Sin pantalla casi.

## 4. Cómo meterlos en el flujo actual (propuesta)

- **Una app por juego puede ser de sensor**: cambiar uno de los 11 puzles de algún juego por uno de esta lista (empezando por los más seguros: *agitar*, *soplar la vela*, *tapar la cámara*, *palmadas*, *brújula*). Se marca con el icono del sensor en la carta y un aviso de permisos en la pantalla del puzle.
- **Cada juego nuevo con 2-3 apps de sensor** y las demás normales, y siempre con el botón de respaldo táctil.
- **Prueba automática:** los solucionadores de Selenium no pueden agitar un móvil real, así que cada app de sensor llevará un modo «simulado» (por URL o botón oculto) que dispara el evento a mano para las pruebas.
- **Primer prototipo sugerido** (bajo coste): un único puzle con micro (silencio + soplar) y otro con acelerómetro (agitar con intensidad), dentro del Faro, para probar permisos en el móvil real de Cristina y Alberto (iPhone y Android) antes de generalizar.

## 5. Respuestas (23 oct 2026)

- **Dispositivos:** iPhone.
- **Formato:** siempre **cartas + móvil**. Como máximo, **móvil + PC** (el Modo PC que ya existe) o **móvil + otro móvil**; nunca un juego solo de móvil ni sin cartas.
- **Consecuencia de diseño:** los puzles de sensor deben funcionar con un solo móvil y, si usan dos dispositivos, el segundo (PC u otro móvil) hace de «segunda pantalla» (muestra la tabla o la mitad del código) sin que el juego dependa de él para avanzar.
