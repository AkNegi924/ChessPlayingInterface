from EvaluationFunctions.MCTS.Mobility import MCTSEngine as MobilityEngine
from EvaluationFunctions.MCTS.KingSafety import MCTSEngine as KingEngine
from EvaluationFunctions.MCTS.MaterialBalance import MCTSEngine as MaterialEngine
from EvaluationFunctions.MCTS.PawnStructure import MCTSEngine as PawnEngine
from EvaluationFunctions.MCTS.PST import MCTSEngine as PSTEngine

import chess
import time
import itertools
import chess.engine
import statistics
import pandas as pd
from tqdm import tqdm


class Tournament:
    def __init__(self):
        # Initialize engines with different evaluation functions
        self.engines = {
            "Mobility": MobilityEngine(),
            "KingSafety": KingEngine(),
            "Material": MaterialEngine(),
            "PawnStructure": PawnEngine(),
            "PST": PSTEngine(),
        }

        # Statistics tracking
        self.stats = {
            name: {
                "wins": 0,
                "losses": 0,
                "draws": 0,
                "eval_times": [],
            }
            for name in self.engines.keys()
        }

        # Create results matrix for win rates
        self.results_matrix = pd.DataFrame(
            0, index=self.engines.keys(), columns=self.engines.keys(), dtype="float64"
        )

    def run_match(self, engine1_name, engine2_name):
        board = chess.Board()
        engine1 = self.engines[engine1_name]
        engine2 = self.engines[engine2_name]

        current_engine = engine1
        current_engine_name = engine1_name

        move_count = 0
        max_moves = 200  # Reduced move limit

        # Initialize progress bar
        with tqdm(
            total=max_moves, desc=f"Match {engine1_name} vs {engine2_name}", unit="move"
        ) as pbar:
            while not board.is_game_over() and move_count < max_moves:
                # Measure evaluation time
                start_time = time.time()
                move = current_engine.get_move(board)
                eval_time = time.time() - start_time

                # Record evaluation time
                self.stats[current_engine_name]["eval_times"].append(eval_time)

                # Make the move
                board.push(move)

                # Update the progress bar
                pbar.update(1)

                # Switch engines
                current_engine = engine2 if current_engine == engine1 else engine1
                current_engine_name = (
                    engine2_name
                    if current_engine_name == engine1_name
                    else engine1_name
                )

                move_count += 1

        # Check if the game was undecided within max_moves
        if move_count >= max_moves and not board.is_game_over():
            # Treat it as a draw
            self.stats[engine1_name]["draws"] += 1
            self.stats[engine2_name]["draws"] += 1
            self.results_matrix.loc[engine1_name, engine2_name] += 0.5
            self.results_matrix.loc[engine2_name, engine1_name] += 0.5
            return "1/2-1/2"

        # Record game result if decided
        result = board.result()
        if result == "1-0":
            self.stats[engine1_name]["wins"] += 1
            self.stats[engine2_name]["losses"] += 1
            self.results_matrix.loc[engine1_name, engine2_name] += 1
        elif result == "0-1":
            self.stats[engine1_name]["losses"] += 1
            self.stats[engine2_name]["wins"] += 1
            self.results_matrix.loc[engine2_name, engine1_name] += 1
        else:
            self.stats[engine1_name]["draws"] += 1
            self.stats[engine2_name]["draws"] += 1
            self.results_matrix.loc[engine1_name, engine2_name] += 0.5
            self.results_matrix.loc[engine2_name, engine1_name] += 0.5

        return result

    # Other methods remain unchanged...

    def run_tournament(self):
        print("Starting tournament...")
        start_time = time.time()

        # Generate all possible pairs of engines
        pairs = list(itertools.combinations(self.engines.keys(), 2))
        total_games = len(pairs) * 2  # *2 for color reversal only
        games_played = 0

        for engine1_name, engine2_name in pairs:
            # Play each pair once with colors reversed
            result = self.run_match(engine1_name, engine2_name)
            games_played += 1
            print(
                f"Game {games_played}/{total_games}: {engine1_name} (White) vs {engine2_name} (Black) - Result: {result}"
            )

            result = self.run_match(engine2_name, engine1_name)
            games_played += 1
            print(
                f"Game {games_played}/{total_games}: {engine2_name} (White) vs {engine1_name} (Black) - Result: {result}"
            )

        end_time = time.time()
        print(f"\nTournament completed in {end_time - start_time:.2f} seconds")

    def generate_report(self):
        print("\n=== Tournament Report ===\n")

        # Calculate and display win rates matrix
        print("\nWin Rates Matrix:")
        total_games_matrix = self.results_matrix + self.results_matrix.T
        win_rate_matrix = (self.results_matrix / total_games_matrix * 100).fillna(0)
        print(win_rate_matrix.round(2))

        # Display detailed statistics for each engine
        print("\nDetailed Engine Statistics:")
        engine_stats = []

        for engine_name, stats in self.stats.items():
            total_games = stats["wins"] + stats["losses"] + stats["draws"]
            win_rate = (stats["wins"] / total_games * 100) if total_games > 0 else 0
            avg_eval_time = (
                statistics.mean(stats["eval_times"]) if stats["eval_times"] else 0
            )

            engine_stats.append(
                {
                    "Engine": engine_name,
                    "Wins": stats["wins"],
                    "Losses": stats["losses"],
                    "Draws": stats["draws"],
                    "Win Rate": f"{win_rate:.2f}%",
                    "Avg Eval Time": f"{avg_eval_time:.3f}s",
                }
            )

        stats_df = pd.DataFrame(engine_stats)
        print(stats_df.to_string(index=False))


if __name__ == "__main__":
    tournament = Tournament()
    tournament.run_tournament()
    tournament.generate_report()
