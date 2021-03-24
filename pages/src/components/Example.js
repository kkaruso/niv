import React from "react";
import ImageGallery from "react-image-gallery";
import exampleOne from "../images/example1_code.png";
import exampleTwo from "../images/example2_command.png";
import exampleThree from "../images/example3_diagramm.png";
import iconCatalog from "../icon_catalog.pdf";
import "./Example.css";
// import Modal from "./Modal";

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
  //   state = {
  //     modal: false,
  //     imageNr: 0,
  //   };

  //   selectModal = (nr) => {
  //     this.setState({
  //       modal: !this.state.modal,
  //       imageNr: nr,
  //     });
  //     console.log(nr);
  //   };

  render() {
    return (
      <div id="example">
        <div className="App">
          {/* <Modal
            displayModal={this.state.modal}
            closeModal={this.selectModal}
            imageNumber={this.imageNr}
          /> */}
        </div>
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
              welche im ganzen Diagramm sichtbar sind. Beim <code>title</code>{" "}
              sind allgemeine Informationen, die unter dem Diagram angezeigt
              werden, vorhanden. In <code>nodes</code>, sind wie der Name schon
              sagt, die einzelnen Nodes bzw. Geräte definiert. In{" "}
              <code>groups</code> kann man Nodes gruppieren. Und schließlich
              sind in&nbsp;
              <code>connections</code> die Verbindungen der jeweiligen Nodes
              definiert. Für jede Node kann man ein Icon, aus einem unserer
              drei&nbsp;
              <a href={iconCatalog} target="_blank" rel="noreferrer">
                Icon-Sets
              </a>
              , auswählen. Außerdem gibt es weitere&nbsp;
              <a href={"src/yaml_parameter/index.html"} target="_blank" rel="noreferrer">
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
              Pfad der YAML-Datei. Der Parameter <code>--detail</code>{" "}
              beschreibt den Detailgrad, also wie viel Informationen tatsächlich
              angezeigt werden. Es gibt noch weitere&nbsp;
              <a href="src/yaml_parameter/index.html" target="_blank">
                Parameter
              </a>
              , welche in unserer Anwendung verwendbar sind.
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
              angegebenen Verbindungen realisiert worden. Die Informationen aus
              dem Titel stehen im unteren Teil des Diagramms. In dem&nbsp;
              <a href="#slider">Bilderslider</a> sieht man auch komplexere
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
