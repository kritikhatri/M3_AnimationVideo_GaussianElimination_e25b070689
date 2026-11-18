# Narration Script - Gaussian Elimination

Read each line while the matching animation plays. Times are from the start of the video.


## Scene 1 - Hook / Context  (0:00.0 - 0:40.0)

- **[0:00.0]** Hi! In this video we'll learn Gaussian elimination, a step-by-step method for solving systems of linear equations.
- **[0:07.8]** Here are three equations in three unknowns, x, y and z. Can you see the solution just by looking? Not really: every equation mixes all three variables.
- **[0:18.3]** Now look at this system. The last equation says seven z equals twenty-one, so z is three. Plug that in above, and y and x follow straight away.
- **[0:27.8]** Here's the surprise: both systems have exactly the same solution. Gaussian elimination is the recipe that turns the hard system into the easy one. Let's see how, and why it works.

## Scene 2 - Concept Introduction  (0:40.0 - 1:36.6)

- **[0:40.0]** First, some notation. Only the numbers matter, not the letters. So we write the system as an augmented matrix: the coefficient matrix A, then a bar, then the right-hand-side column b.
- **[0:51.5]** Each row is one equation: we'll call them R one, R two and R three. Each column belongs to one variable, x, y and z, and the last column holds the constants.
- **[1:02.6]** We are allowed three elementary row operations. One: swap two rows. Two: multiply a row by a non-zero number k. Three: replace a row by itself plus c times another row.
- **[1:15.2]** Our goal is row echelon form, a staircase shape. The first non-zero entry in each row is called a pivot, and every entry below a pivot is zero.
- **[1:24.9]** By the end of this video, you'll be able to reduce a three by three system to echelon form, solve it by back-substitution, and explain why row operations never change the solution.

## Scene 3 - Visual Intuition  (1:36.6 - 2:33.6)

- **[1:36.6]** Before calculating, let's picture it. An equation in three variables is a plane in space. Our three planes meet at a single point, and that point is the solution.
- **[1:46.6]** Now apply our first row operation: R two becomes R two minus two R one. Watch the green plane.
- **[1:53.5]** It tilts to a new position, but it still passes through the same point. Why? If a point satisfies both R one and R two, it automatically satisfies R two minus two R one.
- **[2:05.5]** And the step can be undone: just add two R one back. So no solutions are gained, and none are lost. The solution set is preserved.
- **[2:14.0]** Next, R three minus R one, and then R three minus two R two. Look at the final plane: it is perfectly flat. Seven z equals twenty-one, which is the plane z equals three.
- **[2:26.0]** Every step moved the planes, but never the meeting point. That is the whole idea behind Gaussian elimination.

## Scene 4 - Worked Example  (2:33.6 - 4:06.5)

- **[2:33.6]** Now let's do the algebra carefully. Here is our augmented matrix.
- **[2:37.9]** Step one. The first pivot is the one in the top-left corner. We use it to create zeros below it, in column one.
- **[2:45.2]** To clear the two in row two, subtract two times row one. Two minus two is zero, one minus two is minus one, minus one minus two is minus three, and one minus twelve is minus eleven.
- **[2:57.8]** The new row two replaces the old one.
- **[3:00.3]** For row three, the leading entry is one, so we simply subtract row one. That gives zero, minus two, one, and minus one.
- **[3:07.9]** Column one is now clear. Step two: our next pivot is minus one, in row two, column two.
- **[3:13.9]** To eliminate the minus two below it, use R three minus two R two. Minus two plus two is zero, one plus six is seven, and minus one plus twenty-two is twenty-one.
- **[3:24.9]** And there it is: row echelon form. Three pivots on a staircase, and zeros below every pivot.
- **[3:31.2]** Now solve from the bottom up. This is called back-substitution. The last row says seven z equals twenty-one, so z equals three.
- **[3:39.8]** Row two says minus y minus three z equals minus eleven. Substituting z equals three: minus y minus nine equals minus eleven, so y equals two.
- **[3:50.8]** Row one: x plus two plus three equals six, so x equals one.
- **[3:55.3]** Always check in the original equations. One plus two plus three is six. Two plus two minus three is one. One minus two plus six is five. All three check out.

## Scene 5 - Interpretation  (4:06.5 - 4:58.1)

- **[4:06.5]** So what do these numbers mean? x equals one, y equals two, z equals three is the single point where all three planes meet.
- **[4:14.3]** Echelon form also reveals the structure. Here every column of A has a pivot, so there are no free variables, and the solution is unique.
- **[4:23.0]** But elimination can end differently. Ours ended with a pivot in every column. If instead a row becomes zero, zero, zero, bar five, it says zero equals five. That's impossible, so there is no solution: the planes share no common point.
- **[4:38.9]** And if a row becomes all zeros, including the right-hand side, that equation added no new information. A variable is then free, and there are infinitely many solutions, like planes meeting along a line.
- **[4:51.5]** So after elimination, the pivots tell you everything: one solution, none, or infinitely many.

## Scene 6 - Summary & Credits  (4:58.1 - 5:27.7)

- **[4:58.1]** Let's recap three key takeaways.
- **[5:00.3]** One: write the system as an augmented matrix, A bar b.
- **[5:04.2]** Two: use row operations to reach echelon form. They change the equations, but never the solution set.
- **[5:11.0]** Three: solve by back-substitution, check in the original equations, and read the pivots to know if the solution is unique, impossible, or infinite.
- **[5:20.5]** Thanks for watching! References, tools and the AI disclosure are on screen now.

**Total length: 5:27.7** (1036 words incl. headings)
