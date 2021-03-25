import React from "react";
import ImageGallery from "react-image-gallery";
import exampleOne from "../images/example1_code.png";
import exampleTwo from "../images/example2_command.png";
import exampleThree from "../images/example3_diagramm.png";
import iconCatalog from "../icon_catalog.pdf";
import "./Example.css";

function GetImage(props) {
  return (
    <ImageGallery
      showPlayButton={false}
      useBrowserFullscreen={false}
      showThumbnails={false}
      items={[{ original: props.image }]}
      showFullscreenButton={true}
    />
  );
}

export default class Example extends React.Component {
  render() {
    return (
      <div id="example">
        <div className="App"></div>
        <h2>Beispiel</h2>
        <div class="segment segment-left-to-right">
          <div class="exampleImage">
            <GetImage image={exampleOne} />
          </div>

          <div class="segment-text-left">
            <p>
              Der Benutzer kann eine YAML-Datei erstellen, welche für die
              Erstellung des Diagramms notwendig ist. Die Datei ist sehr simpel
              gehalten. Bei <code>diagram</code> sind Parameter enthalten,
              welche das gesamte Diagramm beeinflussen. Bei <code>title</code>{" "}
              sind Parameter, die den Text unter dem Diagram anpassen. In{" "}
              <code>nodes</code>, sind wie der Name schon sagt, die einzelnen
              Nodes bzw. Geräte definiert. In <code>groups</code> kann man Nodes
              gruppieren. Und schließlich sind in&nbsp;
              <code>connections</code> die Verbindungen zwischen den jeweiligen
              Nodes definiert.
            </p>
            <p>
              {" "}
              Für jede Node kann man ein Icon, aus einem unserer drei&nbsp;
              <a href={iconCatalog} target="_blank" rel="noreferrer">
                Icon-Sets
              </a>
              , auswählen. Außerdem gibt es weitere&nbsp;
              <a
                href="yaml_parameters/index.html"
                target="_blank"
                rel="noreferrer"
              >
                Parameter
              </a>
              , welche die Erstellung des Diagramms erweitern können.
            </p>
          </div>
        </div>

        <div class="segment segment-right-to-left">
          <div class="segment-text-right">
            <p>
              Der Konsolenbefehl setzt sich aus verschiedenen Elementen
              zusammen. Mit <code>niv</code> wird das Programm gestartet,&nbsp;
              <code>--load</code> ist, wie der Name schon verrät, für das Laden
              der YAML-Datei zuständig. Anschließend erfolgt die Angabe über den
              Pfad der YAML-Datei. Der Parameter <br />
              <code>--save</code> ist für das Speichern des erstellten Diagramms
              zuständig. Direkt dahinter wird der Pfad inklusive dem gewünschten
              Dateiname- und format angeben.
            </p>
            <p>
              Für eine Einleitung zum Verwenden des Konsolenbefehls kann man
              sich die{" "}
              <a
                href="https://gitlab.rlp.net/top/21s/niv/niv/-/blob/dev/pages/public/introduction/introduction.md"
                target="_blank"
                rel="noreferrer"
              >
                Ersten Schritte & Installation
              </a>{" "}
              anschauen.
            </p>
          </div>
          <div class="exampleImage">
            <GetImage image={exampleTwo} />
          </div>
        </div>

        <div class="segment segment-left-to-right">
          <div class="exampleImage">
            <GetImage image={exampleThree} />
          </div>
          <div class="segment-text-left">
            <p>
              Das Diagramm ist aus der YAML-Datei entstanden. Hierbei sind alle
              angegebenen Verbindungen realisiert worden, genauso wie die Hintergrundfarbe.
              Die einzelnen Geräte sind richtig gruppiert und visuell voneinander getrennt.
              Die Informationen aus dem Titel stehen im unteren Teil des Diagramms. Ebenso ist "svg" das Dateiformat 
              des Diagramm, wie wir im Schritt davor in der Konsole angegeben haben.
            </p>
            <p>
              In dem&nbsp;
              <a href="#sliderDiv">Bilderslider</a> sieht man auch komplexere
              Diagramme, welche ebenso mit unserem Tool entstanden sind. Da
              diese Diagramme im SVG Format sind, geht die Auflösung nicht
              verloren, wenn die Größe verändert wird.
            </p>
          </div>
        </div>
      </div>
    );
  }
}
