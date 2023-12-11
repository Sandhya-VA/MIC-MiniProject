"""
This is where the implementation of the plugin code goes.
The samplePlugin-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('othelloPlugin')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class othelloPlugin(PluginBase):
  def main(self):
    active_node = self.active_node
    self.namespace=''
    core = self.core
    logger = self.logger
    logger.debug('path: {0}'.format(core.get_path(active_node)))
    logger.info('name: {0}'.format(core.get_attribute(active_node, 'name')))
    logger.warn('pos : {0}'.format(core.get_registry(active_node, 'position')))
    logger.error('guid: {0}'.format(core.get_guid(active_node)))
    nodesList = core.load_sub_tree(active_node)                                          
    nodes = {}  
    for node in nodesList:      
       nodes[core.get_path(node)] = node  
    self.nodes=nodes
    tiles = self.active_tiles()
    logger.info("Total no.of Pieces in Board : {0}".format(self.count_color('black')+self.count_color('white')))
    for t in tiles : 
      pieces=core.get_children_paths(t)
      logger.info("Tile has a piece : {0}".format(pieces))
      t_row=core.get_attribute(t,'row')
      t_col=core.get_attribute(t,'column')
      logger.info("{0},{1} is an active tile".format(t_row,t_col))
      logger.info('This is our last piece played : {0}'.format(core.get_attribute(nodes[core.get_pointer_path(active_node,'lastPiece')],'Piece')))
    #self.flip_lastpiece()
    self.auto()
    next_gs=core.get_pointer_path
    logger.info('This is the next Gamestate : {0}'.format(next_gs))
    self.undo()

  def active_tiles(self):

        def check_valid_tile(tile):
            import math
            active_node = tile
            core = self.core
            logger = self.logger
            self.namespace = None
            META = self.META

            board = core.get_parent(active_node)
            gamestate = core.get_parent(board)
            nodesList = core.load_sub_tree(gamestate)
            nodes = {}

            for node in nodesList:
                nodes[core.get_path(node)] = node

            state = {}
            state['name'] = core.get_attribute(gamestate, 'name')
            logger.info(state)
            cp_path = core.get_pointer_path(gamestate, 'currentPlayer')
            if cp_path is not None:
                state['currentPlayer'] = core.get_attribute(nodes[cp_path], 'name')
            else:
                state['currentPlayer'] = None

            row = core.get_attribute(active_node, 'row')
            column = core.get_attribute(active_node, 'column')
            state['currentMove'] = {'row': row, 'column': column}

            board = [[{'color': 'none'} for _ in range(8)] for _ in range(8)]
            for child in core.get_children_paths(gamestate):
                if (core.is_instance_of(nodes[child], META['Board'])):
                    for tile in core.get_children_paths(nodes[child]):
                        for piece in core.get_children_paths(nodes[tile]):
                            board[core.get_attribute(nodes[tile], 'row')][core.get_attribute(nodes[tile], 'column')][
                                'color'] = core.get_attribute(nodes[piece], 'color')
            state['board'] = board

            def tile_exists(row, col, max_row=7, max_col=7):
                return 0 <= row <= max_row and 0 <= col <= max_col

            def check_logic(state):
                player = state['currentPlayer']
                currentMove = state['currentMove']
                board = state['board']

                currentColor = 'white' if player == 'PlayerBlack' else 'black'
                oppColor = 'black' if currentColor == 'white' else 'white'

                if currentMove is None:
                    return False

                row, col = currentMove['row'], currentMove['column']

                directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
                for d_row, d_col in directions:
                    for k in range(1, 8):
                        new_row, new_col = row + k * d_row, col + k * d_col
                        if not tile_exists(new_row, new_col):
                            break
                        tile_color = board[new_row][new_col]['color']
                        if tile_color == 'none':
                            break
                        if tile_color == oppColor and k == 1:
                            continue
                        if tile_color == currentColor and k > 1:
                            return True
                        break
                return False

            return check_logic(state)

        valid_tiles = []
        cp_list = self.core.get_children_paths(self.active_node)
        self.logger.info('Childs of Game State {0}'.format(cp_list))
        for cp in cp_list:
            child = self.nodes[cp]
            if (self.core.is_instance_of(child, self.META['Board'])):
                for tile in self.core.get_children_paths(self.nodes[cp]):
                    tile = self.nodes[tile]
                    pieces = self.core.get_children_paths(tile)
                    f = self.core.get_attribute(tile, 'pythonCode')
                    row = self.core.get_attribute(tile, 'row')
                    column = self.core.get_attribute(tile, 'column')
                    if row is None or column is None or len(pieces) != 0:
                        continue
                    elif check_valid_tile(tile):
                        valid_tiles.append(tile)
        return valid_tiles

  def count_color(self, color):
        color_count = 0
        cp_list = self.core.get_children_paths(self.active_node)
        for cp in cp_list:
            child = self.nodes[cp]
            if (self.core.is_instance_of(child, self.META['Board'])):
                for tile in self.core.get_children_paths(child):
                    tile = self.nodes[tile]
                    for piece_path in self.core.get_children_paths(tile):
                        piece = self.nodes[piece_path]
                        if color == self.core.get_attribute(piece, 'color'):
                            color_count = color_count + 1
        return color_count

  def flip_lastpiece(self):
        last_piece = self.nodes[self.core.get_pointer_path(self.active_node, 'lastPiece')]
        last_tile = self.core.get_parent(last_piece)

        def check_valid_tile_for_move(tile):
            import math
            active_node = tile
            core = self.core
            logger = self.logger
            self.namespace = None
            META = self.META
            logger.info('Current Node : {0},{1}'.format(core.get_attribute(active_node, 'row'),
                                                        core.get_attribute(active_node, 'column')))
            board = core.get_parent(active_node)
            gamestate = core.get_parent(board)
            nodesList = core.load_sub_tree(gamestate)
            nodes = {}

            for node in nodesList:
                nodes[core.get_path(node)] = node

            state = {}
            state['name'] = core.get_attribute(gamestate, 'name')
            logger.info(state)
            cp_path = core.get_pointer_path(gamestate, 'currentPlayer')
            if cp_path is not None:
                state['currentPlayer'] = core.get_attribute(nodes[cp_path], 'name')
            else:
                state['currentPlayer'] = None
            row = core.get_attribute(active_node, 'row')
            column = core.get_attribute(active_node, 'column')
            state['currentMove'] = {'row': row, 'column': column}

            board = [[{'color': 'none'} for _ in range(8)] for _ in range(8)]
            for child in core.get_children_paths(gamestate):
                if (core.is_instance_of(nodes[child], META['Board'])):
                    for tile in core.get_children_paths(nodes[child]):
                        for piece in core.get_children_paths(nodes[tile]):
                            board[core.get_attribute(nodes[tile], 'row')][
                                core.get_attribute(nodes[tile], 'column')]['color'] = core.get_attribute(
                                nodes[piece], 'color')
            state['board'] = board
            
        def set_nextPlayer(next_gs,next_nodes):
            cp_path=core.get_pointer_path(next_gs,'currentPlayer')
            cp=next_nodes[cp_path]
            for c in core.get_children_paths(next_gs):
              child=next_nodes[c]
              if(core.is_instance_of(child,META['Player']) and child!=cp):
                core.set_pointer(next_gs,'currentPlayer',child)
                np_path=core.get_pointer_path(next_gs,'currentPlayer')
                np=next_nodes[np_path]                
                return core.get_attribute(np,'color')
         
        def set_nextMove(next_gs,next_nodes,pos,player_color):
            next_board=None
            for c in core.get_children_paths(next_gs):
              child=next_nodes[c]
              if(core.is_instance_of(child,META['Board'])):
                next_board=child
              
            for tile in core.get_children_paths(next_board):
              tile=next_nodes[tile]
              next_pos=(core.get_attribute(tile,'row'),core.get_attribute(tile,'column'))
              if next_pos==pos : 
                next_piece=core.create_child(tile,META['Piece'])#usingcopy_node to create a new node
                next_nodes[core.get_path(next_piece)]=next_piece#added piece to next_nodes
                core.set_attribute(next_piece,'color',player_color)
                core.set_pointer(next_gs,'currentMove',next_piece)
                nm_path=core.get_pointer_path(next_gs,'currentMove')
                nm=next_nodes[nm_path]
                return core.get_attribute(nm,'color')
              
        def flip_tiles(next_gs,next_nodes,ft,player_color):
            next_board=None
            flipped_tiles=[]
            for c in core.get_children_paths(next_gs):
              child=next_nodes[c]
              if(core.is_instance_of(child,META['Board'])):
                next_board=child
              
            for tile in core.get_children_paths(next_board):
              tile=next_nodes[tile]
              next_pos=(core.get_attribute(tile,'row'),core.get_attribute(tile,'column'))
              for t in ft :
                if t==next_pos:
                  flip_piece=next_nodes[core.get_children_paths(tile)[0]]
                  core.set_attribute(flip_piece,'color',player_color)
                  flipped_tiles.append(tile)
            return flipped_tiles 
                
            #set_currentMove pointer
            pos=(row,column)
            player_color= core.get_attribute(nodes[cp_path],'color')
            if player_color =='black':
              player_color='white'
            else :
              player_color='black'
            
            def tile_exist(row, col, max_row=7, max_col=7):
                return 0 <= row <= max_row and 0 <= col <= max_col

            def check_logic(state):
                player = state['currentPlayer']
                currentMove = state['currentMove']
                if currentMove is None:
                    return False, []

                board = state['board']
                currentColor = 'white' if player == 'PlayerBlack' else 'black'
                oppColor = 'black' if currentColor == 'white' else 'white'

                tile_flip = []
                directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
                valid_moves = [False for _ in directions]
                tiles_to_flip = [[] for _ in directions]

                for index, (dx, dy) in enumerate(directions):
                    distance = 1
                    while True:
                        new_row, new_col = currentMove['row'] + dx * distance, currentMove['column'] + dy * distance

                        if not tile_exist(new_row, new_col):
                            break
                        tile_color = board[new_row][new_col]['color']

                        if tile_color == 'none':
                            break
                        if tile_color == oppColor:
                            tiles_to_flip[index].append((new_row, new_col))
                        elif tile_color == currentColor and tiles_to_flip[index]:
                            valid_moves[index] = True
                            tile_flip.extend(tiles_to_flip[index])
                            break
                        distance += 1

                is_valid_move = any(valid_moves)
                return is_valid_move, tile_flip

            logger.info('{0} is the next player'.format(set_nextPlayer(next_gs, next_nodes)))
            logger.info('{0} is the next move'.format(set_nextMove(next_gs, next_nodes, pos, player_color)))
            result, ft_pos = check_logic(state)
            ft = flip_tiles(next_gs, next_nodes, ft_pos, player_color)
            logger.info(ft)
            for t in ft:
                flip_piece = next_nodes[core.get_children_paths(t)[0]]
                piece_color = core.get_attribute(flip_piece, 'color')
                logger.info('{0},{1} is the tile with color {2}'.format(core.get_attribute(t, 'row'),
                                                                         core.get_attribute(t, 'column'), piece_color))

            if result:
                self.util.save(self.root_node, self.commit_hash, self.branch_name)
                logger.info('Is a valid move')
            else:
                logger.error('Not a Valid Move')
            return check_logic(state)

        check_valid_tile_for_move(last_tile)
  def auto(self):
      # Helper functions 
      def check_valid(tile):
         
         import math        
         active_node = tile   
         core = self.core             
         logger = self.logger    
         self.namespace = None    
         META = self.META      
         logger.info('Current Node : {0},{1}'.format(core.get_attribute(active_node,'row'),core.get_attribute(active_node,'column')))
         board=core.get_parent(active_node)
         gamestate=core.get_parent(board)
         nodesList = core.load_sub_tree(gamestate)                                          
         nodes = {}  

         for node in nodesList:      
             nodes[core.get_path(node)] = node  


         state = {}        
         state['name'] = core.get_attribute(gamestate, 'name')        
         logger.info(state)        
         cp_path=core.get_pointer_path(gamestate, 'currentPlayer')        
         if cp_path!=None :           
            state['currentPlayer'] = core.get_attribute(nodes[cp_path],'name')        
         else :           
            state['currentPlayer']=None 
         row=core.get_attribute(active_node,'row')
         column=core.get_attribute(active_node,'column')
         state['currentMove']={'row':row,'column':column}        
                
                 
         board = [[{'color': 'none'} for _ in range(8)] for _ in range(8)]        
         for child in core.get_children_paths(gamestate):          
            if (core.is_instance_of(nodes[child], META['Board'])):            
                for tile in core.get_children_paths(nodes[child]):              
                    for piece in core.get_children_paths(nodes[tile]):
                        #logger.info("{0} at {1},{2}".format(core.get_attribute(nodes[piece],'color'),core.get_attribute(nodes[tile],'row'),core.get_attribute(nodes[tile],'column')))
                        
                        board[core.get_attribute(nodes[tile],'row')][core.get_attribute(nodes[tile],'column')]['color'] = core.get_attribute(nodes[piece],'color')
                        #logger.info(board)
         state['board'] = board
         logger.info(state['board'])
         #logger.info(core.get_parent(gamestate))
       
         logger.info("Gamestate nodepath before next{0}".format(gamestate["nodePath"]))
         next_gs = core.copy_node(gamestate,core.get_parent(gamestate))
         core.set_pointer(next_gs,'prev',gamestate)
         next_name=core.get_attribute(gamestate,'name')+str(1)
         core.set_attribute(next_gs,'name',next_name)
         next_nodes={}
         logger.info("Gamestate nodepath after next{0}".format(gamestate["nodePath"]))
         for node in core.load_sub_tree(next_gs) :      
             next_nodes[core.get_path(node)] = node 
              
         
        
         def set_nextPlayer(next_gs,next_nodes):
            cp_path=core.get_pointer_path(next_gs,'currentPlayer')
            cp=next_nodes[cp_path]
            for c in core.get_children_paths(next_gs):
              child=next_nodes[c]
              if(core.is_instance_of(child,META['Player']) and child!=cp):
                core.set_pointer(next_gs,'currentPlayer',child)
                np_path=core.get_pointer_path(next_gs,'currentPlayer')
                np=next_nodes[np_path]                
                return core.get_attribute(np,'color')
         
         def set_nextMove(next_gs,next_nodes,pos,player_color):
            next_board=None
            for c in core.get_children_paths(next_gs):
              child=next_nodes[c]
              if(core.is_instance_of(child,META['Board'])):
                next_board=child
              
            for tile in core.get_children_paths(next_board):
              tile=next_nodes[tile]
              logger.debug(tile['nodePath'])
              logger.debug(next_gs['nodePath'])
              next_pos=(core.get_attribute(tile,'row'),core.get_attribute(tile,'column'))
              if next_pos==pos : 
                next_piece=core.create_child(tile,META['Piece'])#usingcopy_node to create a new node
                #self.logger.info("Tile where piece will be created : {0},{1}".format(pos[0],pos[1]))
                
                next_nodes[core.get_path(next_piece)]=next_piece#added piece to next_nodes
                core.set_attribute(next_piece,'color',player_color)
                core.set_pointer(next_gs,'currentMove',next_piece)
                
                nm_path=core.get_pointer_path(next_gs,'currentMove')
                nm=next_nodes[nm_path]
                return core.get_attribute(nm,'color')
              
         def flip_tiles(next_gs,next_nodes,ft,player_color):
            next_board=None
            flipped_tiles=[]
            for c in core.get_children_paths(next_gs):
              child=next_nodes[c]
              if(core.is_instance_of(child,META['Board'])):
                next_board=child
              
            for tile in core.get_children_paths(next_board):
              tile=next_nodes[tile]
              next_pos=(core.get_attribute(tile,'row'),core.get_attribute(tile,'column'))
              for t in ft :
                if t==next_pos:
                  flip_piece=next_nodes[core.get_children_paths(tile)[0]]
                  core.set_attribute(flip_piece,'color',player_color)
                  flipped_tiles.append(tile)
            return flipped_tiles 
                
            #set_currentMove pointer
         pos=(row,column)
         player_color= core.get_attribute(nodes[cp_path],'color')
         if player_color =='black':
          player_color='white'
         else :
          player_color='black'
         
        
          
        
      def check_logic(state):
        flipped_tiles = []
        current_move = state['currentMove']
        board = state['board']
        current_color = 'white' if state['currentPlayer'] == 'PlayerBlack' else 'black'
        opposite_color = 'black' if current_color == 'white' else 'white'

        if current_move is None:
          return False, flipped_tiles

        row, col = current_move['row'], current_move['column']

        # Directions: right, down, left, up, diag right-down, diag right-up, diag left-down, diag left-up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
          r, c = row + dr, col + dc
          tiles_to_flip = []

        while tile_exist((r, c)) and board[r][c]['color'] == opposite_color:
          tiles_to_flip.append((r, c))
          r += dr
          c += dc

        if tile_exist((r, c)) and board[r][c]['color'] == current_color:
          flipped_tiles.extend(tiles_to_flip)

        is_valid_move = len(flipped_tiles) > 0
        return is_valid_move, flipped_tiles

        def tile_exist(position):
          row, col = position
          return 0 <= row < 8 and 0 <= col < 8
 
        #Auto Move Logic
        logger.info('{0} is the next player'.format(set_nextPlayer(next_gs,next_nodes)))
        logger.info('{0} is the next move'.format(set_nextMove(next_gs,next_nodes,pos,player_color)))       
        result,ft_pos=check_logic(state)
        ft=flip_tiles(next_gs,next_nodes,ft_pos,player_color)
        logger.info(ft)
        for t in ft:
          flip_piece=next_nodes[core.get_children_paths(t)[0]]
          piece_color=core.get_attribute(flip_piece,'color')
          logger.info('{0},{1} is the tile with color {2}'.format(core.get_attribute(t,'row'),core.get_attribute(t,'column'),piece_color))   

          if result : 
            self.util.save(self.root_node,self.commit_hash,self.branch_name)
            logger.info('Is a valid move')
          else : 
            logger.error('Not a Valid Move')
          return  check_logic(state)
      tiles=self.active_tiles()
      if len(tiles)!=0:
        tile=tiles[0]
        t_row=self.core.get_attribute(tile,'row')
        t_col=self.core.get_attribute(tile,'column')
        self.logger.info("{0},{1} is the active tile the AI will play".format(t_row,t_col))
        check_valid(tile)
      else :
        self.logger.info("No more valid moves left")
  def undo(self):
          game_folder=self.core.get_parent(self.active_node)#will be wrong in game folder
          game_state=self.active_node
          #Get the previous state path
          prev_state_path=self.core.get_pointer_path(self.active_node,'prev')
          if prev_state_path is None : 
            self.logger.info("Can't undo initial game state ")
            return
          prev_state = self.core.load_by_path(self.root_node, prev_state_path)
          #Set current state to previous state
          self.core_set_pointer(game_folder,'currentState',prev_state)
          #Delete the current state
          self.core.delete_node(self.active_node)
          #Commit the changes
          self.util.save(self.root_node,self.commit_hash,self.branch_name)