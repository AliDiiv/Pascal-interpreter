# 🐍 Pascal Interpreter

This project is a simple **Pascal Interpreter** written in Python. It allows you to interpret and run Pascal programs directly within the Python environment.

## 🧑‍💻 Features
- Supports basic Pascal syntax such as variables, loops, and conditionals.
- Interprets Pascal code and produces the expected output.
- Easy to modify and extend for additional Pascal features.
- Suitable for educational purposes and learning how interpreters work.

## 📂 Project Structure
- `pascal_interpreter.py`: The main Python script containing the Pascal interpreter logic.
- Example Pascal programs are provided to test the interpreter.

## 🚀 How to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/AliDiiv/Pascal-interpreter.git
    ```

2. Navigate into the project directory:
    ```bash
    cd pascal-interpreter
    ```

3. Run the interpreter with a Pascal file:
    ```bash
    python pascal_interpreter.py example.pas
    ```

## ✨ Usage

You can write Pascal code and run it using this interpreter. For example, the following Pascal code:

```pascal
var
   x:integer;
   y:integer;
begin
  y:=8;
  for x:=y downto 1 do begin
       writeln(x);
  end;
  readln;
end.
