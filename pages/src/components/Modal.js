import React from 'react';
import './Modal.css'

const Modal = props => {

    const divStyle = {
        display: props.displayModal ? 'block' : 'none'
    };
    function closeModal(e) {
        e.stopPropagation()
        props.closeModal()
    }
    return (
        <div
            className="modal"
            onClick={closeModal}
            style={divStyle} >
            <div
                className="modalContent"
                onClick={e => e.stopPropagation()} >
                <span
                    className="close"
                    onClick={closeModal}>&times;
                </span>
                <img className="modalImage" src={props.image} alt="" />

            </div>
        </div>
    );
}
export default Modal;