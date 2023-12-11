import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { icon } from '@fortawesome/fontawesome-svg-core/import.macro';
import { useState } from 'react';
import CONSTANTS from 'constants.js';

export default function Tile({player, piece, position, win}) {

    const [hasMouse, setMouse] = useState(false);

    const onTileClick = () => {
        if (piece === CONSTANTS.PIECE.EMPTY) {
            WEBGME_CONTROL.playerMoves(player, position);
        }
    };

    const onMouseEnter = () => {
        setMouse(true);
    };

    const onMouseLeave = () => {
        setMouse(false);
    };

    const getPieceIcon = () => {
        switch (piece) {
            case CONSTANTS.PIECE.BLACK:
                return icon({name:'circle', family:'classic', style:'solid'});
            case CONSTANTS.PIECE.WHITE:
                return icon({name:'circle', family:'classic', style:'solid'});
            default:
                return null;
        }
    };

    const getPieceStyle = () => {
        return {
            fontSize: '60px',
            color: piece === CONSTANTS.PIECE.BLACK ? 'black' : 'white',
            opacity: hasMouse ? 0.5 : 1,
        };
    };

    const getTileStyle = () => {
        return {
            width: '100px',
            height: '100px',
            backgroundColor: '#0B6623',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            border: '2px solid black',
            boxSizing: 'border-box',
        };
    };

    return (
        <div onClick={onTileClick}
             style={getTileStyle()}
             onMouseEnter={onMouseEnter}
             onMouseLeave={onMouseLeave}>
            {piece !== CONSTANTS.PIECE.EMPTY && (
                <FontAwesomeIcon style={getPieceStyle()} icon={getPieceIcon()} />
            )}
        </div>
    );
}
