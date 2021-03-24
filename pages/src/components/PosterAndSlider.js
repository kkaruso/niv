import React from 'react'
import ImageGallery from 'react-image-gallery';
import poster from '../images/poster.png'
import slide1 from '../images/slide1.png'
import slide2 from '../images/slide2.png'
import slide3 from '../images/slide3.png'
import slide4 from '../images/slide4.png'
import './PosterAndSlider.css';

const images = [
    {
        original: slide1,
        thumbnail: slide1,
    },
    {
        original: slide2,
        thumbnail: slide2,
    },
    {
        original: slide3,
        thumbnail: slide3,
    },
    {
        original: slide4,
        thumbnail: slide4,
    }
];

export default class PosterAndSlider extends React.Component {
    render() {
        return (
            <div id="posterSliderAndMoreLinksDiv">
                <div id="posterAndSliderDiv">

                    <div id="posterDiv">
                        <div class="poster">
                            <h1 ref="image">Werbeposter</h1>
                            <img src={poster} alt="NIV_Poster" id="poster" />
                        </div>
                    </div>
                    <div id="sliderDiv">
                        <h1>Bildslider</h1>
                        <ImageGallery id="slider" items={images} showPlayButton={false} useBrowserFullscreen={false}>

                        </ImageGallery>
                    </div>
                </div>
                <div id="moreLinksDiv">
                    <div id="moreLinks">
                        <h2>Weitere Links</h2>
                        <ul>
                            <li>
                                <a href="https://gitlab.rlp.net/top/21s/niv/niv/-/blob/dev/pages/introduction/introduction.md"
                                    target="_blank" rel="noreferrer">Installation & Erste Schritte</a>
                            </li>
                            <li>
                                <a href="../../yaml_parameters/index.html" target="_blank">YAML Parameter Dokumentation</a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>


        );
    }
}