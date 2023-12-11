import CONSTANTS from 'constants.js';
import Tile from './tile';

export default function Board({player, board, win}) {

    const getTiles = () => {
        const tiles = [];
        board.forEach((value, index) => {
            tiles.push(<Tile key={'tile_' + index} player={player} piece={value} position={index} win={win}/>);
        });

        return tiles;
    }

    return (
        <div style={{
            display:'grid',
            gridTemplateColumns: 'repeat(8, 1fr)', // 8x8 grid for Othello
            gap: '1px', // Adjust gap if necessary for visual separation
            width: '320px', // Adjust the size based on your needs
            backgroundColor: 'green' // Othello boards are traditionally green
        }}>
            {getTiles()}
        </div>
    )
}
