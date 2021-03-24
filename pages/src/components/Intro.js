import React from "react";
import "./Intro.css";

export default class Intro extends React.Component {
  render() {
    return (
      <div id="introduction">
        <div id="intro-text">
          <p>
            Das Projekt "Network Infrastructure Visualizer" zielt darauf ab
            Netzwerkadministratoren bei der Erstellung von Netzwerkdiagrammen zu
            unterstützen, indem es die Möglichkeit bietet YAML-Dateien per
            einfachem Kommandozeilen Aufruf zu detaillierten SVG, PDF sowie
            PNG-Diagramme umzuwandeln. Hierbei ist anzumerken, dass die
            YAML-Dateien einem bestimmten Muster befolgen müssen, welches wir
            detailliert in unserer&nbsp;
            <a href="src/yaml_parameter/index.html" target="_blank">Dokumentation</a> beschrieben haben.
          </p>

          <h3>Problem</h3>
          <p>
            Es gibt ähnliche Produkte bereits auf dem Markt, jedoch fehlt an
            diesen Produkten jeweils der Feinschliff. Unser Produkt ist für den
            Kunden so optimiert, sodass die Interessen widergespiegelt werden.
          </p>
          <h3>Lösung</h3>
          <p>
            Wir haben die verschiedenen Produkte im Detail analysiert, um den
            aktuellen Stand zu erfahren. Anschließend war es uns wichtig, den
            Kundenkontakt zu pflegen, sodass wir regelmäßig an Feedback kommen
            und somit das Produkt anpassen.
          </p>
        </div>
      </div>
    );
  }
}
