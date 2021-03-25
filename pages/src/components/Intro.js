import React from "react";
import "./Intro.css";

export default class Intro extends React.Component {
  render() {
    return (
      <div id="introduction">
        <div id="intro-text">
          <h3>Über unser Projekt</h3>
          <p>
            Das Projekt "Network Infrastructure Visualizer" zielt darauf ab,
            Netzwerkadministratoren bei der Erstellung von Netzwerkdiagrammen zu
            unterstützen, indem es die Möglichkeit bietet, YAML-Dateien per
            einfacher Eingabe in der Kommandozeile zu detaillierten SVG, PDF
            sowie PNG-Diagrammen umzuwandeln. Hierbei ist anzumerken, dass die
            YAML-Dateien einem bestimmten Muster befolgen müssen, welches wir
            detailliert in unserer&nbsp;
            <a href="yaml_parameters/index.html" target="_blank">
              Dokumentation
            </a>{" "}
            beschrieben haben.
          </p>

          <h3>Problem</h3>
          <p>
            Es gibt ähnliche Produkte bereits auf dem Markt, jedoch fehlt an
            diesen Produkten immer irgend etwas, was der Kunde wollte. Zum
            Beispiel fehlte bei einem Produkt das Exportieren von SVG-Diagrammen
            oder die Möglichkeit die Software lokal zu verwenden und somit eine
            Angebundenheit an das Internet eine Voraussetzung ist. Ein weiteres
            Problem war, dass ein anderes Produkt optisch dem Nutzer nicht
            gefallen hat, da das Design vealtet und nicht den Anforderungen
            entsprechend war.
          </p>
          <h3>Lösung</h3>
          <p>
            Wir haben die verschiedenen Produkte im Detail analysiert, um den
            aktuellen Stand zu erfahren. Anschließend war es uns wichtig, den
            Kundenkontakt zu pflegen, sodass wir regelmäßig an Feedback kommen
            und somit das Produkt anpassen. Unser Produkt ist für den Kunden so
            optimiert, sodass die Interessen widergespiegelt werden.
          </p>
        </div>
        <video controls width="640" height="360">
          <source src="../videos/niv_video.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>
    );
  }
}
