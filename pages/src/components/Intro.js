import React from 'react';
import './Intro.css';

export default class Intro extends React.Component {
    render() {
        return (
            <div id="introDiv">
                <div id="intro">
                    <p>
                        Das Projekt "Network Infrastructure Visualizer" unterstütz die
                        visuelle Darstellung einer Netzwerkstruktur mithilfe YAML-Dateien.
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
                        Kundenkontakt zu pflegen, sodass wir regelmäßig an Feedback kommen und
                        somit das Produkt anpassen.
                    </p>
                </div>
            </div>
        );
    }

}