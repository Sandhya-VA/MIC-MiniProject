import React, {useCallback, useState} from 'react';
import Board from './board';
import CONSTANTS from 'constants.js';

export default function Othello({player, win, board}) {
    const getLabel = () => {
        if(!win) {
            let finished = true;
            board.forEach(piece => {
                if(piece === CONSTANTS.PIECE.EMPTY) {
                    finished = false;
                }
            });
            if(finished) {
                return 'Game ended in tie.';
            }
            
            if(player === CONSTANTS.PLAYER.PLYRB) {
                return 'Player Black moves...';
            } else {
                return 'Player White moves...';
            }
        } else {
            if(win.player === CONSTANTS.PLAYER.PLYRB) {
                return 'Player Black won!';
            } else {
                return 'Player White won!';
            }
        }
    }
    return (
    <div style={{ width: '100%', height: '100%', fontFamily:'fantasy', fontSize:'36px', fontWeight:'bold'}}>
        {getLabel()}
        <Board player={player} board={board} win={win}/>
    </div>
    );
}