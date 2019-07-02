import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.stream.Collectors;
import java.util.stream.Stream;
/**
 * 
 * This class Generate Random Graph of linear combination components, and export it to String and CSV File.
 * @paramaters :
 * 		number of inputs to the system
 *      number of components that will be an start components of the system.
 *      number of outputs to the system
 *      
 * @assumptions : 
 * 		Every input go to one component
 *      component that get input, can't receive output from another component, just inputs. 
 *
 *
 */

public class Graph {
	
	private Component [] components ;
	private int number_of_inputs;
	private int number_of_outputs;
	private Random rand = new Random();
	private int num_of_comp_inputs;
	private HashMap<Integer,  Component []> layers;
	private int [] [] many_edges ;

	/**
	 * Constructor
	 * @param nunmber_of_inputs
	 * @param number_of_outputs
	 * @param components
	 * @param num_of_comp_inputs
	 */
	public Graph(int nunmber_of_inputs , int number_of_outputs, Component [] components, int num_of_comp_inputs){
		this.number_of_inputs = nunmber_of_inputs;
		this.number_of_outputs = number_of_outputs;
		this.components = cloneArray(components);
		this.num_of_comp_inputs = num_of_comp_inputs;
		this.layers = new HashMap<Integer, Component[]>();
		this.many_edges = new int [components.length][components.length];
		
	}
	/**
	 * Kind of Main Function.
	 * @throws Exception
	 */
	public void generate_random_graph() throws Exception{
		divide_to_layers();
		System.out.println("End Layers");
		set_as_outputs();
		System.out.println("End Outputs");
		set_randomize_edges();
		System.out.println("End Edges");

		updated_deadends_components();
		System.out.println("End deadend");

		givenDataArray_whenConvertToCSV_thenOutputCreated(toString_arrays_list());
		System.out.println("End Convert");

	}
	
	private void divide_to_layers() throws Exception{
		Random rnd = new Random();
		Component [] layer_1 = new Component[num_of_comp_inputs];
		int counter_layer =2;
		if(num_of_comp_inputs > components.length){
			throw new Exception("There are too many input components");
		}
		if(num_of_comp_inputs > number_of_component_with_one_input()){
			throw new Exception("There are too many input components");
		}
		for(int i=0; i< num_of_comp_inputs; i++){
			int index = rnd.nextInt(components.length);
			while(Arrays.asList(layer_1).contains( components[index]) || components[index].get_number_of_inputs() > 1){
				index = rnd.nextInt(components.length);
			}
			layer_1[i] = components[index];
			components[index].set_line_number(1);
			components[index].set_as_input();
		}
		layers.put(1, layer_1);
		while(components.length - number_of_component_in_hash(layers) >= 1){
			if(rnd.nextInt(2)>0){
				int number_in_this_layer = rnd.nextInt(components.length - number_of_component_in_hash(layers)) +1 ;
				Component [] arr = new Component[number_in_this_layer];
				for(int i=0; i< number_in_this_layer ; i++){
					Component c = get_component_not_in_hash(layers);
					arr[i] = c;
					c.set_line_number(counter_layer);
				}
				layers.put(counter_layer, arr);
				counter_layer++;
			}
			else{
				int sum_in_this_layer = 0;
				for(int i=0; i< components.length ; i++){
					if(components[i].get_line_number() == -1)
						sum_in_this_layer++;
				}
				Component [] arr = new Component[sum_in_this_layer];
				int counter = 0;
				for(int i=0; i< components.length ; i++){
					if(components[i].get_line_number() == -1){
						arr[counter] = components[i];
						components[i].set_line_number(counter_layer);
					}
				}
				layers.put(counter_layer, arr);

			}
			
		}
	}
	private int number_of_component_with_one_input(){
		int ans =0;
		for(int i=0; i<components.length;i++){
			if(components[i].get_number_of_inputs() ==1)
				ans ++;
		}
		return ans;
	}
	
	private void set_as_outputs() throws Exception{
		if(number_of_outputs > components.length)
			throw new Exception("there are more outputs components than number of components.");
		for(Component c : layers.get(layers.size())){
			c.set_as_output();
		}
		if(this.number_of_outputs > layers.get(layers.keySet().size()).length){
			Random rnd = new Random();
			for(int i =0 ; i< number_of_outputs -  layers.get(layers.keySet().size()).length ; i++){
				int index = rnd.nextInt(components.length);
				while(components[index].is_output()){
					index = rnd.nextInt(components.length);
				}
				components[index].set_as_output();
			}
		}
	}
	private void set_randomize_edges(){
		Random rnd = new Random();
		int counter =0;
		/*for(Component c : layers.get(1)){
			Component child = components[rnd.nextInt(components.length)];
			while(child.get_line_number() <= c.get_line_number() || child.getParents().size()  == child.get_number_of_inputs()){
				child = components[rnd.nextInt(components.length)];
			}
			c.add_child(child);
			child.add_parent(c);
		}
		System.out.println("first loop");*/
		for(Integer key: layers.keySet()){
			if(counter !=0){
				for(Component c : layers.get(key)){
					if(c.get_number_of_inputs() > c.getParents().size()){
						int nump = c.getParents().size();
						for(int i=0; i< c.get_number_of_inputs()-  nump; i++){
							Component parent = components[rnd.nextInt(components.length)];
							while(parent.get_line_number() >= c.get_line_number()){
								 parent = components[rnd.nextInt(components.length)];
							}
							if(c.getParents().contains(parent) || parent.getChilds().contains(c)){
								many_edges[indexOf(c,components)][indexOf(parent,components)]++;
							}
							c.add_parent(parent);
							parent.add_child(c);
						}
					}
				}
			}
			counter ++;
		}
		
	}
	
	private Component  get_component_not_in_hash( HashMap<Integer, Component []> map){
		for(Component c : components){
			if(! in_hashmap(c, layers)){
				return c;
			}
		}
		return null;
	}
	
	private boolean in_hashmap (Component c , HashMap<Integer, Component []> map){
		
		for(Integer key: map.keySet()){
			if(Arrays.asList(map.get(key)).contains(c))
				return true;
		}
		return false;
	}
	
	private int number_of_component_in_hash(HashMap<Integer, Component []> map){
		int sum =0;
		for(Integer key: map.keySet()){
			sum += map.get(key).length;
		}
		return sum;
	}

		
	/**
	 * Function that change component to be output if he dose'nt have childrens
	 * This function help to avoid from possible deadends in the system. 
	 * 
	 */
	private void updated_deadends_components(){
		for(Component c : components){
			if(c.getChilds().isEmpty())
				c.set_as_output();
		}
	}
	private Component [] cloneArray( Component [] arr){
		Component [] new_arr = new Component [arr.length];
		for (int i=0; i< arr.length ; i++){
			new_arr[i] = new Component(arr[i]);
		}
		return new_arr;
	}
	/**
	 * Function That Translate the graph to string.
	 */
	
	public String toString(){
		String ans = "";
		String input_components = "";
		String output_components = "";
		String edges = "";
		
		for(Component c : components){
			if(c.is_input())
				input_components += c.get_linear_equation()+ " , ";
		}
		
		for(Component c : components){
			if(c.is_output())
				output_components += c.get_linear_equation() + " , ";
		}
		output_components = output_components.substring(0, output_components.length() -2);
		input_components = input_components.substring(0 , input_components.length() -2);
		/*for(Component c : components){
			for (Integer index : c.getIndexsOfInputs()){
				edges +=  "Input number" + index.toString() +"  ->  " + c.get_linear_equation() + " ; "	;

			}
		}
		*/
		for(Component c : components){
			for (Component child : c.getChilds()){
				edges +=  c.get_linear_equation() + "  ->  " + child.get_linear_equation() + " ; "	;
			}
		}
		
		edges = edges.substring(0, edges.length() );
		ans = "Inputs: " + input_components + "\n" + "Outputs: " +output_components + "\n" + "Edges: " +edges;
		System.out.println(ans);
		return ans;
	}
	/**
	 * Function that translate the graph to List<String []> , for that we can generate the CSV file.
	 * @return
	 */
	public List<String[]> toString_arrays_list(){
		int [] [] indexs_of_edges = new int [components.length][getMaxNumOfInputs()];
		for(int i =0; i< components.length ; i++){
			for (int j=0 ; j< getMaxNumOfInputs() ; j++){
				indexs_of_edges[i][j] =-1;
			}
		}
		change_components_series ();
		List<String[]> dataLines = new ArrayList<>();
		String [] comp_names = new String [components.length +2];
		comp_names[0] = "";
		comp_names[components.length +1] = "";
		int index=1;
		for(Component c : components){
			comp_names[index] = c.get_linear_equation();
			index++;
		}
		dataLines.add(comp_names);
		
		for(Component c : components){
			String [] comp_line = new String [components.length +2];
			comp_line [0] = c.get_linear_equation();
			int i=1;
			for(Component neighboor : components ){
				if (c.getParents().contains(neighboor)){
					int edge_num = rand.nextInt(c.get_number_of_inputs()) +1;
					while(is_index_edge_in_use(indexs_of_edges , edge_num , i))
						edge_num = rand.nextInt(c.get_number_of_inputs()) +1;
					indexs_of_edges[i][return_next_free_place(indexs_of_edges, i)] = edge_num;
					if(many_edges[indexOf(c,components)][indexOf(neighboor,components)] > 0){
						String ans = "0";
						for(int k=0 ; k< many_edges[indexOf(c,components)][indexOf(neighboor,components)] ; k++ ){
							ans+= ", "+ (k+1);
						}
						comp_line[i] = ans;
					}
					else{
						comp_line[i] = "" +(edge_num-1);
					}
				}
				else{
					comp_line[i] = "-1";
				}
				i++;
			}
			if(c.is_input())
				comp_line[components.length +1] = "TRUE";
			else
				comp_line[components.length +1] = "FALSE";
			dataLines.add(comp_line);
		}
		String [] comp_outputs = new String [components.length +2];
		index=1;
		comp_outputs[0] = "";
		comp_outputs[components.length +1] = "";
		for(Component c : components){
			if(c.is_output())
				comp_outputs[index] = "TRUE";
			else
				comp_outputs[index] = "FALSE";
			index++;
		}
		dataLines.add(comp_outputs);
		return remove_nulls_from_list(dataLines);
	}

	private void change_components_series(){
		for(int i=0; i< components.length; i++){
			if(components[i].getChilds().isEmpty()){
				for(int j= components.length-1; j>=0 ; j-- ){
					if(!components[j].getChilds().isEmpty()){
						Component c = components[j];
						components[j] = components[i];
						components[i] = c;
					}
					break;
				}
			}
		}
	}
	
	private List<String []> remove_nulls_from_list (List<String []> list){
		for(String [] e : list){
			if(e == null){
				list.remove(e);
			}
		}
		return list;
	}
	
	private int return_next_free_place(int [] [] arr , int index_component){
		for(int i =0 ; i < getMaxNumOfInputs() ; i++){
			if(arr[index_component][i] == -1)
				return i;
		}
		return -1;
	}
	
	private boolean is_index_edge_in_use(int [] [] arr , int index_edge ,int index_component){
		for(int i=0; i< getMaxNumOfInputs() ; i++){
			if(arr[index_component][i] == index_edge)
				return true;
		}
		return false;
	}
	
	private int getMaxNumOfInputs(){
		int max = 0;
		for(Component c : components){
			if (c.get_number_of_inputs() >  max)
				max = c.get_number_of_inputs();
		}
		return max;
	}
	/**
	 * Generate CSV From List<String []>
	 * @param dataLines
	 * @throws IOException
	 */
	public void givenDataArray_whenConvertToCSV_thenOutputCreated(List <String []> dataLines) throws IOException {
	    File csvOutputFile = new File("SystemModule.csv");
	    try (PrintWriter pw = new PrintWriter(csvOutputFile)) {
	        dataLines.stream()
	          .map(this::convertToCSV)
	          .forEach(pw::println);
	    }
	}
	
	public String convertToCSV(String[] data) {
	    return Stream.of(data)
	      .map(this::escapeSpecialCharacters)
	      .collect(Collectors.joining(","));
	}
	
	public String escapeSpecialCharacters(String data) {
	    String escapedData = data.replaceAll("\\R", " ");
	    if (data.contains(",") || data.contains("\"") || data.contains("'")) {
	        data = data.replace("\"", "\"\"");
	        escapedData = "\"" + data + "\"";
	    }
	    return escapedData;
	}
	
	public long factorialUsingForLoop(int n) {
	    long fact = 1;
	    for (int i = 2; i <= n; i++) {
	        fact = fact * i;
	    }
	    return fact;
	}
	
	public static <T> int indexOf(T needle, T[] haystack)
	{
	    for (int i=0; i<haystack.length; i++)
	    {
	        if (haystack[i] != null && haystack[i].equals(needle)
	            || needle == null && haystack[i] == null) return i;
	    }

	    return -1;
	}

}
