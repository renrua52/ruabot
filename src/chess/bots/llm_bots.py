from openai import OpenAI
import openai
import os
import time



from chess.game.player import Player

class LLMBot(Player):
    def __init__(self, model_name):
        super().__init__(f'LLM Bot: {model_name}')
        self.model_name = model_name

        self.client = OpenAI(
            api_key = os.environ.get('OPENAI_API_KEY'),
            base_url = os.environ.get('OPENAI_API_BASE')
        )

    

    def chat(self, prompt):
        max_retries = 5
        retries = 0
        completion = ""
        system_prompt = "You are a helpful assistant."
        while retries < max_retries:
            try:
                completion = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                )
                break
            except openai.RateLimitError as e:
                print(f"Attempt {retries+1}/{max_retries} failed. Retrying...")
                retries += 1
                time.sleep(2)
        else:
            print("Failed calling API.")
        
        return completion.choices[0].message.content


    def generateMove(self, position):
        grid = position.getGrid()
        color = 'white' if position.turn == 'w' else 'black'

        prompt = f"""You are a professional chess grandmaster.

Here is a chess position from the perspective of the white player. Letters means corresponding pieces in standard chess notation, uppercase for white and lowercase for black. For example, 'n' means a black knight. The symbol '*' represents empty square.

## Position

{grid}

"""
        
        if position.enpassant != '-':
            prompt += f"""In the current position, you do have the right to do an en-passant move. The en-passant square is {position.enpassant}\n"""

        for castle in ['O-O', 'O-O-O']:
            if position.canCastle(castle):
                prompt += f"""In the current position, you do have the right to make the move {castle}.\n"""

        prompt += f"""If not specified, you cannot do en-passant or castling.

You have to play the {color} pieces. Find the best legal move for {color}. For your reference, all legal moves are listed below:

## Legal Moves

{str(position.allLegalMoves())}



Your answer can be written in standard chess notation, or you can just select one in the list provided.

In your answer, wrap the move you are going to make in <MOVE></MOVE>"""
        

        print(prompt)
        print()
        response = self.chat(prompt)
        print(response)
        print()

        
        import re
        pattern = r'<MOVE>(.*?)</MOVE>'
        move = re.findall(pattern, response, re.DOTALL)[0]

        return move