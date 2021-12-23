program Main;
   var c : integer;

function PythagorasFunc(A: Real; B: Real) : Real; { The pythagoras theorem }
begin
	PythagorasFunc := A * A + B * B;
	{ Output: Assign the function name to the value.
	If you forget to assign the function to the value,
	you will get a trash value from memory }
end; { PythagorasFunc }

procedure Alpha(a : integer; b : integer);
var x : integer;

   procedure Beta(a : integer; b : integer);
   var x, y : integer;
   begin
      x := a * 10 + b * 2 + c * 2;
      y := x;
   end;

begin
   x := (a + b) * 2;

   Beta(5, 10);      { procedure call }
end;

begin { Main }
   c := 20;
   Alpha(3 + 5, 7);  { procedure call }

end.  { Main }