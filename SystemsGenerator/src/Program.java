import java.util.Scanner;
import java.util.Random;

public class Program {
	/**
	 * This Function is the Main FUnction.
	 * @param args
	 * @throws Exception
	 *  syste, gen , problem gen , daignoss.
	 */
	public static void main (String [] args) throws Exception{
		Scanner in = new Scanner(System.in);
		
		System.out.println("************************************* Hello (_._) *************************************");
		
		System.out.println("\nPlease enter number of Components: ");
	 	int num_of_comps = in.nextInt();
		Component [] comps = new Component [num_of_comps];
		System.out.println("Please enter number of Components That you want to be an input Component to the system: ");
	 	int num_of_comp_inputs = in.nextInt();
		System.out.println("Please enter number of inputs of the system: ");
	 	int num_of_inputs = in.nextInt();
		System.out.println("Please enter number of outputs of the system: ");
	 	int num_of_outputs = in.nextInt();
	 	in.nextLine();
	 	System.out.println("please enter number of component with one argument:");
		int num_of_args = in.nextInt();
		int counter =0;
	 	for(int i=0; i< num_of_args ; i++){
			String [] Arg = new String [1];
			for (int j =0;j< 1 ; j++){
				Arg[j] = "x"+j;
			}
			Component c = new Component(Arg, generate_linear_equation(1));
			comps[counter] = c;
			counter++;
	 	}
	 	System.out.println("please enter number of component with two argument:");
		num_of_args = in.nextInt();
	 	for(int i=0; i< num_of_args ; i++){
			String [] Arg = new String [2];
			for (int j =0;j< 2 ; j++){
				Arg[j] = "x"+j;
			}
			Component c = new Component(Arg, generate_linear_equation(2));
			comps[counter] = c;
			counter++;
		}
	 	
	 	System.out.println("please enter number of component with three argument:");
		num_of_args = in.nextInt();
	 	for(int i=0; i< num_of_args ; i++){
			String [] Arg = new String [3];
			for (int j =0;j< 3 ; j++){
				Arg[j] = "x"+j;
			}
			Component c = new Component(Arg, generate_linear_equation(3));
			comps[counter] = c;
			counter++;
		}

	 	Graph graph = new Graph(num_of_inputs, num_of_outputs, comps , num_of_comp_inputs);
	 	graph.generate_random_graph();
	 	System.out.println(graph.toString());
	}
	
	public static String generate_linear_equation(int number_of_components){
		Random rand = new Random();
		String equation = "";
		for(int i =0 ; i<= number_of_components ; i++){
			if(i != number_of_components){
				int multiplaier = rand.nextInt(9) +1;
				equation += multiplaier + "*x" + i + " ";
				int operator = rand.nextInt(2);
				if(operator == 0){
					equation += "+ -";
				}
				else{
					equation += "+ ";
				}

			}
			else{
				int multiplaier = rand.nextInt(9) +1;
				equation += multiplaier;
			}
		}
		return equation;
	}
	
}
