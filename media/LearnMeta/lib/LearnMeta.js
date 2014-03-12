/* start module: LearnMeta */
$pyjs['loaded_modules']['LearnMeta'] = function (__mod_name__) {
	if($pyjs['loaded_modules']['LearnMeta']['__was_initialized__']) return $pyjs['loaded_modules']['LearnMeta'];
	var $m = $pyjs['loaded_modules']['LearnMeta'];
	$m['__repr__'] = function() { return '<module: LearnMeta>'; };
	$m['__was_initialized__'] = true;
	if ((__mod_name__ === null) || (typeof __mod_name__ == 'undefined')) __mod_name__ = 'LearnMeta';
	$m['__name__'] = __mod_name__;


	$m['pyjd'] = $p['___import___']('pyjd', null);
	$m['Button'] = $p['___import___']('pyjamas.ui.Button.Button', null, null, false);
	$m['RootPanel'] = $p['___import___']('pyjamas.ui.RootPanel.RootPanel', null, null, false);
	$m['Label'] = $p['___import___']('pyjamas.ui.Label.Label', null, null, false);
	$m['Grid'] = $p['___import___']('pyjamas.ui.Grid.Grid', null, null, false);
	$m['CellFormatter'] = $p['___import___']('pyjamas.ui.CellFormatter.CellFormatter', null, null, false);
	$m['RowFormatter'] = $p['___import___']('pyjamas.ui.RowFormatter.RowFormatter', null, null, false);
	$m['HTML'] = $p['___import___']('pyjamas.ui.HTML.HTML', null, null, false);
	$m['CheckBox'] = $p['___import___']('pyjamas.ui.CheckBox.CheckBox', null, null, false);
	$m['AbsolutePanel'] = $p['___import___']('pyjamas.ui.AbsolutePanel.AbsolutePanel', null, null, false);
	$m['Window'] = $p['___import___']('pyjamas.Window', null, null, false);
	$m['Timer'] = $p['___import___']('pyjamas.Timer.Timer', null, null, false);
	$m['logging'] = $p['___import___']('pyjamas.logging', null, null, false);
	$m['log'] = $m['logging']['getConsoleLogger']();
	$m['State'] = $p['___import___']('learning.State', null, null, false);
	$m['ab'] = $p['___import___']('learning.ab', null, null, false);
	$m['is_win'] = $p['___import___']('learning.is_win', null, null, false);
	$m['is_full'] = $p['___import___']('learning.is_full', null, null, false);
	$m['turn'] = $p['___import___']('learning.turn', null, null, false);
	$m['is_over'] = $p['___import___']('learning.is_over', null, null, false);
	$m['normalize'] = $p['___import___']('learning.normalize', null, null, false);
	$m['td_learning'] = $p['___import___']('learning.td_learning', null, null, false);
	$m['find_last_move'] = $p['___import___']('learning.find_last_move', null, null, false);
	$m['INCREMENT_AMOUNT'] = 0.05;
	$m['GridWidget'] = (function(){
		var $cls_definition = new Object();
		var $method;
		$cls_definition['__module__'] = 'LearnMeta';
		$method = $pyjs__bind_method2('__init__', function() {
			if (this['__is_instance__'] === true) {
				var self = this;
			} else {
				var self = arguments[0];
			}
			var $add2,$add3,$add1,$add4,explanation;
			self['state'] = $m['State']();
			self['game_round'] = 0;
			self['TD_CONSTS'] = $p['dict']([['c3', 1.0], ['c2', 1.0], ['c1', 1.0], ['c6', 1.0], ['c5', 1.0], ['c4', 1.0]]);
			self['CONSTS'] = $p['dict']([['c3', 0.5], ['c2', 1.0], ['c1', 3.0], ['c6', 0.5], ['c5', 0.5], ['c4', 0.5]]);
			self['BEST_CONSTANTS'] = $p['dict']([['c3', 0.767944], ['c2', 1.049451], ['c1', 3.074038], ['c6', 0.220823], ['c5', 0.281883], ['c4', 0.605861]]);
			self['ONES_CONSTS'] = $p['dict']([['c3', 1.0], ['c2', 1.0], ['c1', 1.0], ['c6', 1.0], ['c5', 1.0], ['c4', 1.0]]);
			$m['AbsolutePanel']['__init__'](self);
			self['welcome_label'] = $m['HTML']('To watch the AI play itself, press either "begin game" button.');
			self['add']($p['getattr'](self, 'welcome_label'));
			self['depth_limit'] = 2;
			self['new_game'] = $m['Button']('New game', self);
			self['add']($p['getattr'](self, 'new_game'));
			self['train_td'] = $m['Button']('Begin game.  Learning AI first!', self);
			self['add']($p['getattr'](self, 'train_td'));
			self['train_static'] = $m['Button']('Begin game.  Static AI first!', self);
			self['add']($p['getattr'](self, 'train_static'));
			self['score_label'] = $m['Label']($p['sprintf']('CURRENT SCORE: Learning AI: %d | Static AI: %d', $p['tuple']([0, 0])));
			self['add']($p['getattr'](self, 'score_label'));
			self['increase_depth'] = $m['Button']('Increase ply search depth.', self);
			self['decrease_depth'] = $m['Button']('Decrease ply search depth.', self);
			self['depth_label'] = $m['Label']($p['__op_add']($add3=$p['__op_add']($add1='Current depth is ',$add2=$p['str']($p['getattr'](self, 'depth_limit'))),$add4='.'));
			self['depth_grid'] = $m['Grid']();
			self['depth_grid']['resize'](1, 3);
			self['depth_grid']['setBorderWidth'](2);
			self['depth_grid']['setCellPadding'](9);
			self['depth_grid']['setCellSpacing'](1);
			self['add']($p['getattr'](self, 'depth_grid'));
			self['depth_grid']['setWidget'](0, 0, $p['getattr'](self, 'decrease_depth'));
			self['depth_grid']['setWidget'](0, 1, $p['getattr'](self, 'depth_label'));
			self['depth_grid']['setWidget'](0, 2, $p['getattr'](self, 'increase_depth'));
			self['g'] = $m['Grid']();
			self['g']['resize'](3, 3);
			self['g']['setBorderWidth'](2);
			self['g']['setCellPadding'](9);
			self['g']['setCellSpacing'](1);
			self['init']();
			self['add']($p['getattr'](self, 'g'));
			self['adj_grid'] = $m['Grid']();
			self['adj_grid']['resize'](7, 4);
			self['adj_grid']['setBorderWidth'](2);
			self['adj_grid']['setCellPadding'](9);
			self['adj_grid']['setCellSpacing'](1);
			self['init_constants_adj_grid']();
			self['add']($p['getattr'](self, 'adj_grid'));
			self['reset_constants'] = $m['Button']("Reset all of Learning AI's constants to 1.", self);
			self['add']($p['getattr'](self, 'reset_constants'));
			self['state_to_grid']();
			explanation = '\n<div style="margin-top: 1em;width: 90%;margin-left: 5%;">\n\n<p>\n<h3>Rules of the Game</h3>\nMeta-tic-tac-toe is played on a board consisting of 9 different tic-tac-toe boards, each of which can be won independently.  Boards are won in an identical fashion to tic-tac-toe, and like tic-tac-toe, turns alternate between player one <em>(1\'s)</em> and player two <em>(2\'s)</em>.  Once a board has been won or is full of pieces, neither player can play into it.  The nine boards are arranged in a three by three grid pattern with the coordinate of the previous move\ndetermining which board the next player can play into. (Example: a place into the <em>center</em> position of any of the nine tic-tac-toe boards means that the next player must play into the <em>central</em> tic-tac-toe board.)  The first player to move must play into the center board.  If a player is supposed to play into a board which has already been won or is completely full of pieces, he/she instead chooses which of the remaining boards to play into and plays in an empty position in\nit.  Play is stopped when all individual boards have been won or are completely full of pieces.  At this point, the agent with the most points wins.\n</p>\n\n<p>\n<h3>Turning Python into JavaScript with pyjs/pyjamas</h3>\nThe AI for this game is programmed in python.  During initial development, the only interface to play the AI was through the python terminal.  When I decided to expand this project into a web app, I had to choose whether the AI would run on the client or the server.  I quickly decided that this computationally intensive task should be put client side which necessitated somehow transforming my python script into javascript.  I realized that I\ncould translate my python code into javascript manually, but a superior solution would be finding an adequate python to javascript compiler/translator.  Pyjs/pyjamas seemed adequate for this job, and it also provides a convenient library for creating a user interface.  Indeed, pyjs/pyjamas has been able to do everything I needed it to do, but if I had to start over again, I would probably <em>not</em> use pyjs/pyjamas.  Due to cryptic or non existent error messages, debugging pyjs/pyjamas is an\narduous process.  Indeed, the most difficult step was the initial translation of my python script into javascript which required a substantial change in my existing implementation to get around a <a href="https://github.com/pyjs/pyjs/issues/817">bug</a>.  In addition to cryptic error messages, the output of the pyjs/pyjamas compiler is extremely slow and innefficient. While the python CLI AI can perform a minimax search to a depth of 5 ply, the pyjs/pyjamas AI in the same time can only search to a depth\nof 3.  As a result, the AI for this web app has an inferior skill relative to the command line interface AI.\n</p>\n\n<p>\n<a name="depth_explanation"></a>\n<h3>How the AI Works</h3>\nThe AI uses the <a href="http://en.wikipedia.org/wiki/Minimax">minimax</a> search algorithm to find a next move.  Basically the AI looks at all the possible moves that the player MAX can make (player MAX because the current player is trying to maximize the utility of its move), and selects the move with the highest predicted utility.  How does the player MAX calculate the predicted utility of a move or state?  Player MAX makes a recursive call to the minimax algorithm, except,\nthis time the next player will be player MIN who is trying to minimize the utility of the positions.  Player MIN, like player MAX looks at all the possible moves, but choses the move with the lowest predicted utility.  How does player MIN calculate the predicted utility of a move?  Well you can already guess: making a recursive call to the minimax algorithm.  However, at some point these recursive calls must stop, so an additional parameter is passed into the minimax algorithm that\nkeeps track of depth.  When the maximum depth has been reached, the minimax algorithm, rather than making a recursive call to itself, makes a call to a utility function that assigns a rough estimate of the value of the state.\n</p>\n\n<p>\n<a name="utility_function"></a>\n<h3>The Utility Function</h3>\nThe utility function looks at a given state and using some heuristics assigns an approximate value to the state.  Oftentimes a utility function is composed of a number of basis functions.  The return value of each basis function is then multiplied by some constant and then the whole thing is added together:\n<Pre style="white-space: pre-wrap;">\ndef utility(state):\n  v1 = basis_1(state) * c1\n  v2 = basis_2(state) * c2\n  .\n  .\n  .\n\n  vn = basis_n(state) * cn\n  return v1 + v2 + ...  + vn\n</Pre>\nFor a more familiar game like chess, one can imagine these basis functions being based on a number of things including the relative number of pieces that each player has.  For instance, if relative number of pawns basis function is multiplied by a constant equal to 1, then the relative number of rooks basis function should be multiplied by a constant equal to 5 according to <a href="http://en.wikipedia.org/wiki/Chess_strategy#Basic_concepts_of_board_evaluation">chess strategy</a>.  In\nthe case of meta tic-tac-toe, my utility function is based on six different basis functions:\n<li>\n<em>f1_score</em> (multiplied by Constant 1) - the relative "score" of each player.  This is calculated by subtracting the score of player MIN from the score of player MAX.\n</li>\n<li>\n<em>f2_center</em> (multiplied by Constant 2) - the relative number of center pieces.  This is calculated by subtracting the number of center pieces that MIN has from the number of center pieces that MAX has.\n</li>\n<li>\n<em>f3_corner</em> (multiplied by Constant 3) - the relative number of corner pieces (e.g. top right).\n</li>\n<li>\n<em>f4_side</em> (multiplied by Constant 4) - the relative number of side pieces (e.g. top middle).\n</li>\n<li>\n<em>f5_blocking</em> (multiplied by Constant 5) - the relative number of blocking positions.  For example any time there are three pieces in a row/column/diagonal that are not all of the same type, that is considered a blocking position.\n</li>\n<li>\n<em>f6_potential</em> (multiplied by Constant 6) - the relative number of potential positions.  Any position that could lead to a three in a row, at the next opportunity is considered a potential position.\n</li>\nThese six basis functions are components of the utility function, but they should not be weighted equally.\n<em>f1_score</em>, is clearly much more important than <em>f4_side</em>.  In fact, in my implementation, <em>f1_score</em> is 3.07:0.61 times more important than <em>f4_side</em>.  One can experiment with how changing these constants will change the behavior of the AI.  However, without a lengthy analysis, the precise weighting is difficult to determine.  To determine these constants analytically, I used temporal difference learning.\n</p>\n\n<p>\n<h3>Learning Utility Function Constants Using Temporal Difference Learning</h3>\n<a href="http://en.wikipedia.org/wiki/Temporal_difference_learning">Temporal difference learning</a> works by comparing two evaluations of the utility of a state: one evaluation that is not very ideal and the other evaluation that is somehow closer to the true value.  Then the constants are updated so that if the less ideal evaluation were computed again, it would return a value closer to what the more idea evaluation had returned.  In my case, one evaluation is simply the utility function applied to the current state, and the other evaluation that is somehow\nmore "ideal" is what the minimax search predicts\nwill occur -- in other words, it is the utility function evaluation of the state that the minimax search predicts will be played.  (In a sense, temporal difference learning is vaguely analogous to supervised learning except rather than having labeled/training instances, we have these more "ideal" predictions based on using the minimax search.)  My implementation of temporal difference learning is expressed in only a few lines of python code:\n<Pre style="white-space: pre-wrap;">\ndef td_learning(terminal_state, TD_CONSTS, prev_state):\n  \'\'\'This function modifies TD_CONSTS according to the temporal difference algorithm.\n  TD_CONSTS: the constants multiplied by the basis functions to compute the utility function.\n  prev_state: the current state that the minimax search has just found a next move for.\n  terminal_state: the state that the minimax search predicts will occur\n  if both players play ideally.\n  This state is not the state that the AI choses as its next move, but rather the state that the minimax search predicts will\n  occur in the future if both players play ideally.\n\n  Note: the number of moves between prev_state and terminal_state is equal to the number of ply searched,\n  e.g. the depth_limit parameter passed to the minimax search function, ab.\n  \'\'\'\n  change_total_utility = utility(terminal_state, TD_CONSTS) - utility(prev_state, TD_CONSTS)\n  sub1 = sub_utility(terminal_state, TD_CONSTS)\n  sub2 = sub_utility(prev_state, TD_CONSTS)\n  change_sub_utility = [ (sub1[i] - sub2[i]) for i in range(len(sub1)) ]\n  for i in range(len(TD_CONSTS)):\n    TD_CONSTS[\'c\' + str(i+1)] += ALPHA * change_total_utility * (change_sub_utility[i]) * (-1)\n\n  # normalize\n  TD_CONSTS = normalize(TD_CONSTS)\n  return TD_CONSTS\n</Pre>\nThe <a href="http://chet-weger.herokuapp.com/learn_meta_ttt/">training regime</a> proceeds by playing a game where the AI makes moves for both sides.  After only a few games of training, one can see dramatic improvements in the relative value of the constants.  After about 15-20 training games, the learning AI is typically capable of beating the static AI.  Figure 1 shows how the static AI\'s constants improve over a series of twenty training games.  In this\nseries of games, both AIs search to a depth of 3 ply, and the static AI\'s constants are the same as the default values in this application (i.e. they are {\'c1\':3, \'c2\':2, \'c3\':0.5, \'c4\':0.5, \'c5\':0.5, \'c6\':0.5}). Notice that the static AI\nstarts by consistently beating the learning AI, but the last 5 games are all won by the learning AI.  Other patterns are also noticeable from the graph.  The ending moves of a game tend to produce the most change in the constants.  This makes sense because most of the points in a game are typically won in the last quarter of a game.  When points are being won rapidly, then the difference between the predicted utility and the actual utility will be at its highest.\n</p>\n</div>\n<p>\n<img width="1700" align="middle" src="http://chet-weger.herokuapp.com/media/imgs/temporal_difference_learning_in_meta_ttt.png"></img>\n</p>\n\n\n<br>\n</div>\n\n<p align="center">Written by <a href="http://chet-weger.herokuapp.com/">Chet Weger</a>.  Questions, comments, bugs?  Contact me at chetweger [at] gmail.com.</p>\n<p align="center"><a href="http://chet-weger.herokuapp.com/">Return to my home page.</a></p>\n    ';
			self['add']($m['HTML'](explanation));
			return null;
		}
	, 1, [null,null,['self']]);
		$cls_definition['__init__'] = $method;
		$method = $pyjs__bind_method2('init_constants_adj_grid', function() {
			if (this['__is_instance__'] === true) {
				var self = this;
			} else {
				var self = arguments[0];
			}
			var j,$iter1_nextval,static_ai_header,$iter1_idx,td_keys,learning_ai_header,$iter1_iter,i,$add6,$iter1_array,key,$add5,$iter1_type;
			self['decr_buttons'] = $p['dict']([]);
			self['adj_learning_labels'] = $p['dict']([]);
			self['adj_static_labels'] = $p['dict']([]);
			self['incr_buttons'] = $p['dict']([]);
			td_keys = $p['list'](['c1', 'c2', 'c3', 'c4', 'c5', 'c6']);
			learning_ai_header = $m['Label']('Constant for the learning AI.');
			self['adj_grid']['setWidget'](0, 0, learning_ai_header);
			static_ai_header = $m['Label']('Constants for the static AI.');
			self['adj_grid']['setWidget'](0, 2, static_ai_header);
			$iter1_iter = $p['enumerate'](td_keys);
			$iter1_nextval=$p['__iter_prepare']($iter1_iter,false);
			while (typeof($p['__wrapped_next']($iter1_nextval)['$nextval']) != 'undefined') {
				var $tupleassign1 = $p['__ass_unpack']($iter1_nextval['$nextval'], 2, null);
				i = $tupleassign1[0];
				key = $tupleassign1[1];
				j = $p['__op_add']($add5=i,$add6=1);
				$p['getattr'](self, 'adj_learning_labels')['__setitem__'](key, $m['Label']($p['sprintf']('Constant %d: %f', $p['tuple']([key['__getitem__'](1), $p['getattr'](self, 'TD_CONSTS')['__getitem__'](key)]))));
				self['adj_grid']['setWidget'](j, 0, $p['getattr'](self, 'adj_learning_labels')['__getitem__'](key));
				$p['getattr'](self, 'decr_buttons')['__setitem__'](key, $m['Button']('<', self));
				self['adj_grid']['setWidget'](j, 1, $p['getattr'](self, 'decr_buttons')['__getitem__'](key));
				$p['getattr'](self, 'adj_static_labels')['__setitem__'](key, $m['Label']($p['sprintf']('Constant %d: %f', $p['tuple']([key['__getitem__'](1), $p['getattr'](self, 'CONSTS')['__getitem__'](key)]))));
				self['adj_grid']['setWidget'](j, 2, $p['getattr'](self, 'adj_static_labels')['__getitem__'](key));
				$p['getattr'](self, 'incr_buttons')['__setitem__'](key, $m['Button']('>', self));
				self['adj_grid']['setWidget'](j, 3, $p['getattr'](self, 'incr_buttons')['__getitem__'](key));
			}
			return null;
		}
	, 1, [null,null,['self']]);
		$cls_definition['init_constants_adj_grid'] = $method;
		$method = $pyjs__bind_method2('init', function() {
			if (this['__is_instance__'] === true) {
				var self = this;
			} else {
				var self = arguments[0];
			}
			var $iter5_nextval,y_cell,$iter5_array,$iter3_type,$iter5_iter,$iter4_type,$iter5_type,$iter4_iter,$iter3_idx,$iter2_iter,$iter3_iter,$iter5_idx,x_board,$iter2_type,$iter2_idx,b,$iter3_array,y_board,$iter2_nextval,g,$iter4_nextval,$iter4_idx,x_cell,$iter4_array,$iter3_nextval,$iter2_array;
			$iter2_iter = $p['range'](3);
			$iter2_nextval=$p['__iter_prepare']($iter2_iter,false);
			while (typeof($p['__wrapped_next']($iter2_nextval)['$nextval']) != 'undefined') {
				y_board = $iter2_nextval['$nextval'];
				$iter3_iter = $p['range'](3);
				$iter3_nextval=$p['__iter_prepare']($iter3_iter,false);
				while (typeof($p['__wrapped_next']($iter3_nextval)['$nextval']) != 'undefined') {
					x_board = $iter3_nextval['$nextval'];
					g = $m['Grid']();
					g['resize'](3, 3);
					g['setBorderWidth'](2);
					g['setCellPadding'](9);
					g['setCellSpacing'](1);
					$iter4_iter = $p['range'](3);
					$iter4_nextval=$p['__iter_prepare']($iter4_iter,false);
					while (typeof($p['__wrapped_next']($iter4_nextval)['$nextval']) != 'undefined') {
						x_cell = $iter4_nextval['$nextval'];
						$iter5_iter = $p['range'](3);
						$iter5_nextval=$p['__iter_prepare']($iter5_iter,false);
						while (typeof($p['__wrapped_next']($iter5_nextval)['$nextval']) != 'undefined') {
							y_cell = $iter5_nextval['$nextval'];
							b = $m['Button']('AI could play here.', self);
							b['point'] = $p['dict']([['x_cell', x_cell], ['y_cell', y_cell], ['y_board', y_board], ['x_board', x_board]]);
							g['setWidget'](y_cell, x_cell, b);
						}
					}
					self['add'](g);
					self['g']['setWidget'](y_board, x_board, g);
				}
			}
			return null;
		}
	, 1, [null,null,['self']]);
		$cls_definition['init'] = $method;
		$method = $pyjs__bind_method2('start_new_game', function() {
			if (this['__is_instance__'] === true) {
				var self = this;
			} else {
				var self = arguments[0];
			}

			$m['g']['state'] = $m['State']();
			$m['g']['game_over'] = false;
			self['depthLimit'] = 2;
			self['human_first'] = true;
			self['check_is_win']();
			self['max_player'] = '-1';
			self['min_player'] = '-1';
			self['state_to_grid']();
			return null;
		}
	, 1, [null,null,['self']]);
		$cls_definition['start_new_game'] = $method;
		$method = $pyjs__bind_method2('onClick', function(sender) {
			if (this['__is_instance__'] === true) {
				var self = this;
			} else {
				var self = arguments[0];
				sender = arguments[1];
			}
			var $add14,$add15,$add16,$add10,$add7,$add12,$add13,$sub2,$add8,$add9,$sub1,$add11;
			self['check_adjusts'](sender);
			if ($p['bool']($p['op_eq'](sender, $p['getattr'](self, 'reset_constants')))) {
				self['TD_CONSTS'] = $p['getattr'](self, 'ONES_CONSTS');
				self['sync_consts']();
			}
			if ($p['bool']($p['op_eq'](sender, $p['getattr'](self, 'increase_depth')))) {
				self['depth_limit'] = $p['__op_add']($add7=$p['getattr'](self, 'depth_limit'),$add8=1);
				self['depth_label']['setText']($p['__op_add']($add11=$p['__op_add']($add9='Current depth is ',$add10=$p['str']($p['getattr'](self, 'depth_limit'))),$add12='.'));
			}
			if ($p['bool']($p['op_eq'](sender, $p['getattr'](self, 'decrease_depth')))) {
				self['depth_limit'] = $p['__op_sub']($sub1=$p['getattr'](self, 'depth_limit'),$sub2=1);
				self['depth_label']['setText']($p['__op_add']($add15=$p['__op_add']($add13='Current depth is ',$add14=$p['str']($p['getattr'](self, 'depth_limit'))),$add16='.'));
			}
			if ($p['bool']($p['op_eq'](sender, $p['getattr'](self, 'new_game')))) {
				self['start_new_game']();
			}
			if ($p['bool']($p['op_eq'](sender, $p['getattr'](self, 'train_td')))) {
				self['state'] = $m['State']();
				self['static_ai_str'] = '2';
				self['td_ai_str'] = '1';
				$p['getattr'](self, 'state')['next_piece'] = $p['list']([1, 1, 1]);
				$pyjs_kwargs_call(null, $m['Timer'], null, null, [{'notify':$p['getattr'](self, 'td_ai_turn')}, 250]);
			}
			if ($p['bool']($p['op_eq'](sender, $p['getattr'](self, 'train_static')))) {
				self['state'] = $m['State']();
				self['static_ai_str'] = '1';
				self['td_ai_str'] = '2';
				$p['getattr'](self, 'state')['next_piece'] = $p['list']([1, 1, 1]);
				$pyjs_kwargs_call(null, $m['Timer'], null, null, [{'notify':$p['getattr'](self, 'static_ai_turn')}, 250]);
			}
			return null;
		}
	, 1, [null,null,['self'],['sender']]);
		$cls_definition['onClick'] = $method;
		$method = $pyjs__bind_method2('check_adjusts', function(sender) {
			if (this['__is_instance__'] === true) {
				var self = this;
			} else {
				var self = arguments[0];
				sender = arguments[1];
			}
			var $iter6_idx,td_keys,$iter6_type,$iter6_array,key,$iter6_iter,$iter6_nextval;
			td_keys = $p['list'](['c1', 'c2', 'c3', 'c4', 'c5', 'c6']);
			$iter6_iter = td_keys;
			$iter6_nextval=$p['__iter_prepare']($iter6_iter,false);
			while (typeof($p['__wrapped_next']($iter6_nextval)['$nextval']) != 'undefined') {
				key = $iter6_nextval['$nextval'];
				if ($p['bool']($p['op_eq']($p['getattr'](self, 'incr_buttons')['__getitem__'](key), sender))) {
					self['change_td_const'](key, '+');
				}
				if ($p['bool']($p['op_eq']($p['getattr'](self, 'decr_buttons')['__getitem__'](key), sender))) {
					self['change_td_const'](key, '-');
				}
				self['TD_CONSTS'] = $m['normalize']($p['getattr'](self, 'TD_CONSTS'));
				$p['getattr'](self, 'adj_learning_labels')['__getitem__'](key)['setText']($p['sprintf']('Constant %d: %f', $p['tuple']([key['__getitem__'](1), $p['getattr'](self, 'TD_CONSTS')['__getitem__'](key)])));
			}
			self['sync_consts']();
			return null;
		}
	, 1, [null,null,['self'],['sender']]);
		$cls_definition['check_adjusts'] = $method;
		$method = $pyjs__bind_method2('change_td_const', function(key, sign) {
			if (this['__is_instance__'] === true) {
				var self = this;
			} else {
				var self = arguments[0];
				key = arguments[1];
				sign = arguments[2];
			}
			var $augexpr1,$augexpr2,$augsub2,$augsub1,$add17,$sub3,$add18,$sub4;
			if ($p['bool']($p['op_eq'](sign, '+'))) {
				var $augsub1 = key;
				var $augexpr1 = $p['getattr'](self, 'CONSTS');
				$augexpr1['__setitem__']($augsub1, $p['__op_add']($add17=$augexpr1['__getitem__']($augsub1),$add18=$m['INCREMENT_AMOUNT']));
			}
			else if ($p['bool']($p['op_eq'](sign, '-'))) {
				var $augsub2 = key;
				var $augexpr2 = $p['getattr'](self, 'CONSTS');
				$augexpr2['__setitem__']($augsub2, $p['__op_sub']($sub3=$augexpr2['__getitem__']($augsub2),$sub4=$m['INCREMENT_AMOUNT']));
			}
			return null;
		}
	, 1, [null,null,['self'],['key'],['sign']]);
		$cls_definition['change_td_const'] = $method;
		$method = $pyjs__bind_method2('sync_consts', function() {
			if (this['__is_instance__'] === true) {
				var self = this;
			} else {
				var self = arguments[0];
			}
			var $iter7_nextval,td_keys,$iter7_iter,$iter7_array,key,$iter7_idx,$iter7_type;
			td_keys = $p['list'](['c1', 'c2', 'c3', 'c4', 'c5', 'c6']);
			$iter7_iter = td_keys;
			$iter7_nextval=$p['__iter_prepare']($iter7_iter,false);
			while (typeof($p['__wrapped_next']($iter7_nextval)['$nextval']) != 'undefined') {
				key = $iter7_nextval['$nextval'];
				$p['getattr'](self, 'adj_learning_labels')['__getitem__'](key)['setText']($p['sprintf']('Constant %d: %f', $p['tuple']([key['__getitem__'](1), $p['getattr'](self, 'TD_CONSTS')['__getitem__'](key)])));
				$p['getattr'](self, 'adj_static_labels')['__getitem__'](key)['setText']($p['sprintf']('Constant %d: %f', $p['tuple']([key['__getitem__'](1), $p['getattr'](self, 'CONSTS')['__getitem__'](key)])));
			}
			return null;
		}
	, 1, [null,null,['self']]);
		$cls_definition['sync_consts'] = $method;
		$method = $pyjs__bind_method2('check_is_win', function(last_position) {
			if (this['__is_instance__'] === true) {
				var self = this;
			} else {
				var self = arguments[0];
				last_position = arguments[1];
			}
			if (typeof last_position == 'undefined') last_position=arguments['callee']['__args__'][3][1];
			var static_ai_score,$add21,$add20,$add22,$add25,$add24,$add26,game_over_message,msg,learning_ai_score,$add19,$add23;
			$pyjs_kwargs_call(self, 'state_to_grid', null, null, [{'prev_x_board':last_position['__getitem__']('x_board'), 'prev_y_board':last_position['__getitem__']('y_board'), 'prev_x_cell':last_position['__getitem__']('x_cell'), 'prev_y_cell':last_position['__getitem__']('y_cell')}]);
			learning_ai_score = $p['getattr']($p['getattr'](self, 'state'), 'score')['__getitem__']($p['getattr'](self, 'td_ai_str'));
			static_ai_score = $p['getattr']($p['getattr'](self, 'state'), 'score')['__getitem__']($p['getattr'](self, 'static_ai_str'));
			self['score_label']['setText']($p['sprintf']('CURRENT SCORE: Learning AI(%d): %d | Static AI(%d): %d', $p['tuple']([$p['getattr'](self, 'td_ai_str'), learning_ai_score, $p['getattr'](self, 'static_ai_str'), static_ai_score])));
			self['state']['printInfo']();
			if ($p['bool']($m['is_over']($p['getattr'](self, 'state')))) {
				if ($p['bool'](($p['cmp'](learning_ai_score, static_ai_score) == 1))) {
					msg = $p['sprintf']('the learning AI won with score %d vs %d.', $p['tuple']([learning_ai_score, static_ai_score]));
				}
				else if ($p['bool'](($p['cmp'](learning_ai_score, static_ai_score) == -1))) {
					msg = $p['sprintf']('the static AI won with score %d vs %d.', $p['tuple']([static_ai_score, learning_ai_score]));
				}
				else if ($p['bool']($p['op_eq'](learning_ai_score, static_ai_score))) {
					msg = 'the game ended in a tie.';
				}
				self['game_round'] = $p['__op_add']($add19=$p['getattr'](self, 'game_round'),$add20=1);
				game_over_message = $m['Label']($p['__op_add']($add25=$p['__op_add']($add23=$p['__op_add']($add21='In game round ',$add22=$p['str']($p['getattr'](self, 'game_round'))),$add24=', '),$add26=msg));
				self['add'](game_over_message);
				return true;
			}
			else {
				return false;
			}
			return null;
		}
	, 1, [null,null,['self'],['last_position', $p['dict']([])]]);
		$cls_definition['check_is_win'] = $method;
		$method = $pyjs__bind_method2('static_ai_turn', function() {
			if (this['__is_instance__'] === true) {
				var self = this;
			} else {
				var self = arguments[0];
			}
			var over,next_state,last_position,expectedUtility;
			$p['printFunc'](['\n\nNaive AIs turn which plays the piece: ', $p['getattr']($p['getattr'](self, 'state'), 'next_piece')['__getitem__'](2)], 1);
			$p['printFunc'](['next piece is ', $p['getattr']($p['getattr'](self, 'state'), 'next_piece')], 1);
			$p['printFunc'](['TD_CONSTS', $p['getattr'](self, 'TD_CONSTS')], 1);
			var $tupleassign2 = $p['__ass_unpack']($pyjs_kwargs_call(null, $m['ab'], null, null, [{'depth_limit':$p['getattr'](self, 'depth_limit')}, $p['getattr'](self, 'state'), $p['getattr'](self, 'CONSTS')]), 2, null);
			expectedUtility = $tupleassign2[0];
			next_state = $tupleassign2[1];
			last_position = $m['find_last_move']($p['getattr'](self, 'state'), next_state);
			self['state'] = next_state;
			self['state']['printInfo']();
			over = self['check_is_win'](last_position);
			$p['printFunc'](['back in static'], 1);
			if ($p['bool'](!$p['bool'](over))) {
				self['pause_update'] = $pyjs_kwargs_call(null, $m['Timer'], null, null, [{'notify':$p['getattr'](self, 'td_ai_turn')}, 250]);
			}
			else {
				return true;
			}
			return null;
		}
	, 1, [null,null,['self']]);
		$cls_definition['static_ai_turn'] = $method;
		$method = $pyjs__bind_method2('td_ai_turn', function() {
			if (this['__is_instance__'] === true) {
				var self = this;
			} else {
				var self = arguments[0];
			}
			var expectedUtility,over,state,last_position,terminal_state;
			$p['printFunc'](['\n\nTD AI player starting turn. TD AI places the piece:', $p['getattr']($p['getattr'](self, 'state'), 'next_piece')['__getitem__'](2)], 1);
			$p['printFunc'](['TD_CONSTS after being adjusted are: ', $p['getattr'](self, 'TD_CONSTS')], 1);
			var $tupleassign3 = $p['__ass_unpack']($pyjs_kwargs_call(null, $m['ab'], null, null, [{'depth_limit':$p['getattr'](self, 'depth_limit')}, $p['getattr'](self, 'state'), $p['getattr'](self, 'TD_CONSTS')]), 2, null);
			expectedUtility = $tupleassign3[0];
			state = $tupleassign3[1];
			terminal_state = $p['getattr'](expectedUtility, 'terminal');
			self['TD_CONSTS'] = $m['td_learning'](terminal_state, $p['getattr'](self, 'TD_CONSTS'), $p['getattr'](self, 'state'));
			self['sync_consts']();
			last_position = $m['find_last_move']($p['getattr'](self, 'state'), state);
			self['state'] = state;
			state['printInfo']();
			$p['printFunc'](['TD_CONSTS after being adjusted are: ', $p['getattr'](self, 'TD_CONSTS')], 1);
			over = self['check_is_win'](last_position);
			$p['printFunc'](['back in td'], 1);
			$p['printFunc'](['Is over ', over], 1);
			if ($p['bool'](!$p['bool'](over))) {
				return $pyjs_kwargs_call(null, $m['Timer'], null, null, [{'notify':$p['getattr'](self, 'static_ai_turn')}, 250]);
			}
			else {
				return true;
			}
			return null;
		}
	, 1, [null,null,['self']]);
		$cls_definition['td_ai_turn'] = $method;
		$method = $pyjs__bind_method2('will_buttons', function(y_board, x_board) {
			if (this['__is_instance__'] === true) {
				var self = this;
			} else {
				var self = arguments[0];
				y_board = arguments[1];
				x_board = arguments[2];
			}
			var piece,$or1,$or2,$and1,$and3,$and4,board,playable,$and2;
			board = $p['getattr']($p['getattr'](self, 'state'), 'boards');
			piece = $p['list']($p['getattr']($p['getattr'](self, 'state'), 'next_piece'));
			playable = true;
			if ($p['bool'](($p['bool']($or1=$m['is_win'](board['__getitem__'](piece['__getitem__'](0))['__getitem__'](piece['__getitem__'](1))))?$or1:$m['is_full'](board['__getitem__'](piece['__getitem__'](0))['__getitem__'](piece['__getitem__'](1)))))) {
				playable = false;
			}
			if ($p['bool'](($p['bool']($and1=!$p['bool']($m['is_win'](board['__getitem__'](y_board)['__getitem__'](x_board))))?!$p['bool']($m['is_full'](board['__getitem__'](y_board)['__getitem__'](x_board))):$and1))) {
				if ($p['bool'](!$p['bool'](playable))) {
					return true;
				}
				if ($p['bool'](playable)) {
					return ($p['bool']($and3=$p['op_eq'](y_board, piece['__getitem__'](0)))?$p['op_eq'](x_board, piece['__getitem__'](1)):$and3);
				}
			}
			return false;
		}
	, 1, [null,null,['self'],['y_board'],['x_board']]);
		$cls_definition['will_buttons'] = $method;
		$method = $pyjs__bind_method2('state_to_grid', function(prev_x_board, prev_y_board, prev_x_cell, prev_y_cell) {
			if (this['__is_instance__'] === true) {
				var self = this;
			} else {
				var self = arguments[0];
				prev_x_board = arguments[1];
				prev_y_board = arguments[2];
				prev_x_cell = arguments[3];
				prev_y_cell = arguments[4];
			}
			if (typeof prev_x_board == 'undefined') prev_x_board=arguments['callee']['__args__'][3][1];
			if (typeof prev_y_board == 'undefined') prev_y_board=arguments['callee']['__args__'][4][1];
			if (typeof prev_x_cell == 'undefined') prev_x_cell=arguments['callee']['__args__'][5][1];
			if (typeof prev_y_cell == 'undefined') prev_y_cell=arguments['callee']['__args__'][6][1];
			var will_make_buttons,$iter10_nextval,y_cell,$iter8_iter,$iter10_iter,$iter9_iter,$iter9_nextval,$iter9_idx,board,$iter11_idx,$iter9_type,x_board,$and8,$and9,$iter8_idx,x_cell,$iter11_iter,$iter8_type,$iter10_idx,$and5,$and6,$and7,$and12,$and10,$and11,$iter8_nextval,$iter11_array,$iter11_nextval,y_board,b,g,$iter11_type,$iter8_array,$iter10_array,$iter10_type,$iter9_array;
			board = $p['getattr']($p['getattr'](self, 'state'), 'boards');
			$iter8_iter = $p['range'](3);
			$iter8_nextval=$p['__iter_prepare']($iter8_iter,false);
			while (typeof($p['__wrapped_next']($iter8_nextval)['$nextval']) != 'undefined') {
				y_board = $iter8_nextval['$nextval'];
				$iter9_iter = $p['range'](3);
				$iter9_nextval=$p['__iter_prepare']($iter9_iter,false);
				while (typeof($p['__wrapped_next']($iter9_nextval)['$nextval']) != 'undefined') {
					x_board = $iter9_nextval['$nextval'];
					will_make_buttons = self['will_buttons'](y_board, x_board);
					g = $m['Grid']();
					g['resize'](3, 3);
					g['setBorderWidth'](2);
					g['setCellPadding'](9);
					g['setCellSpacing'](1);
					$iter10_iter = $p['range'](3);
					$iter10_nextval=$p['__iter_prepare']($iter10_iter,false);
					while (typeof($p['__wrapped_next']($iter10_nextval)['$nextval']) != 'undefined') {
						y_cell = $iter10_nextval['$nextval'];
						$iter11_iter = $p['range'](3);
						$iter11_nextval=$p['__iter_prepare']($iter11_iter,false);
						while (typeof($p['__wrapped_next']($iter11_nextval)['$nextval']) != 'undefined') {
							x_cell = $iter11_nextval['$nextval'];
							if ($p['bool']($p['op_eq'](board['__getitem__'](y_board)['__getitem__'](x_board)['__getitem__'](y_cell)['__getitem__'](x_cell)['__getitem__']('cell'), 0))) {
								if ($p['bool'](will_make_buttons)) {
									b = $m['HTML']($p['sprintf']('<p style="color:blue">AI %d could<br>play here.</p>', $p['getattr']($p['getattr'](self, 'state'), 'next_piece')['__getitem__'](2)), self);
								}
								else {
									b = $m['HTML']('-');
								}
							}
							else if ($p['bool']($p['op_eq'](board['__getitem__'](y_board)['__getitem__'](x_board)['__getitem__'](y_cell)['__getitem__'](x_cell)['__getitem__']('cell'), 1))) {
								if ($p['bool'](($p['bool']($and5=$p['op_eq'](prev_x_cell, x_cell))?($p['bool']($and6=$p['op_eq'](prev_y_cell, y_cell))?($p['bool']($and7=$p['op_eq'](prev_y_board, y_board))?$p['op_eq'](prev_x_board, x_board):$and7):$and6):$and5))) {
									b = $m['HTML']('<p style="color:red">1</p>');
								}
								else {
									b = $m['HTML']('1');
								}
							}
							else if ($p['bool']($p['op_eq'](board['__getitem__'](y_board)['__getitem__'](x_board)['__getitem__'](y_cell)['__getitem__'](x_cell)['__getitem__']('cell'), 2))) {
								if ($p['bool'](($p['bool']($and9=$p['op_eq'](prev_x_cell, x_cell))?($p['bool']($and10=$p['op_eq'](prev_y_cell, y_cell))?($p['bool']($and11=$p['op_eq'](prev_y_board, y_board))?$p['op_eq'](prev_x_board, x_board):$and11):$and10):$and9))) {
									b = $m['HTML']('<p style="color:red">2</p>');
								}
								else {
									b = $m['HTML']('2');
								}
							}
							g['setWidget'](y_cell, x_cell, b);
						}
					}
					self['add'](g);
					self['g']['setWidget'](y_board, x_board, g);
				}
			}
			return null;
		}
	, 1, [null,null,['self'],['prev_x_board', (typeof ($usub1=1)=='number'?
			-$usub1:
			$p['op_usub']($usub1))],['prev_y_board', (typeof ($usub2=1)=='number'?
			-$usub2:
			$p['op_usub']($usub2))],['prev_x_cell', (typeof ($usub3=1)=='number'?
			-$usub3:
			$p['op_usub']($usub3))],['prev_y_cell', (typeof ($usub4=1)=='number'?
			-$usub4:
			$p['op_usub']($usub4))]]);
		$cls_definition['state_to_grid'] = $method;
		var $bases = new Array($m['AbsolutePanel']);
		var $data = $p['dict']();
		for (var $item in $cls_definition) { $data['__setitem__']($item, $cls_definition[$item]); }
		return $p['_create_class']('GridWidget', $p['tuple']($bases), $data);
	})();
	if ($p['bool']($p['op_eq']((typeof __name__ == "undefined"?$m['__name__']:__name__), '__main__'))) {
		$m['pyjd']['setup']('./GridTest.html');
		$m['g'] = $m['GridWidget']();
		$m['r'] = $m['RootPanel']();
		$m['r']['add']($m['g']);
		$m['pyjd']['run']();
	}
	return this;
}; /* end LearnMeta */


/* end module: LearnMeta */


/*
PYJS_DEPS: ['pyjd', 'pyjamas.ui.Button.Button', 'pyjamas', 'pyjamas.ui', 'pyjamas.ui.Button', 'pyjamas.ui.RootPanel.RootPanel', 'pyjamas.ui.RootPanel', 'pyjamas.ui.Label.Label', 'pyjamas.ui.Label', 'pyjamas.ui.Grid.Grid', 'pyjamas.ui.Grid', 'pyjamas.ui.CellFormatter.CellFormatter', 'pyjamas.ui.CellFormatter', 'pyjamas.ui.RowFormatter.RowFormatter', 'pyjamas.ui.RowFormatter', 'pyjamas.ui.HTML.HTML', 'pyjamas.ui.HTML', 'pyjamas.ui.CheckBox.CheckBox', 'pyjamas.ui.CheckBox', 'pyjamas.ui.AbsolutePanel.AbsolutePanel', 'pyjamas.ui.AbsolutePanel', 'pyjamas.Window', 'pyjamas.Timer.Timer', 'pyjamas.Timer', 'pyjamas.logging', 'learning.State', 'learning', 'learning.ab', 'learning.is_win', 'learning.is_full', 'learning.turn', 'learning.is_over', 'learning.normalize', 'learning.td_learning', 'learning.find_last_move']
*/
