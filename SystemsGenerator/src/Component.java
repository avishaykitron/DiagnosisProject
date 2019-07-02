import java.util.ArrayList;
import java.util.List;
/**
 * 
 *
 * This class Represent an Component Of Linear Equation. 
 */
public class Component {
	/**
	 * The Fields of this class Are:
	 * {@link #number_of_inputs} That Represent The number of Arguments That this component used to get.
	 * {@link #parents} The Components that transfer to him thier output
	 * {@link #childs} The Components that this component transfer to them his output.
	 * {@link #inputs_indexes} The indexes of inputs that going throws this component.
	 * {@link #linear_equation} The datum of this component
	 * {@link #is_input} & {@link #is_output} boolean fields that represent if this component is in/out of the system.
	 * {@link #line_number} represent the layer of the component in the system.

	 */
	private int number_of_inputs = 0;
	private String [] arguments ;
	private String linear_equation ;
	private boolean is_input = false;
	private boolean is_output = false;
	private List<Component> parents;
	private List<Component> childs;
	private List<Integer> inputs_indexes ;
	private int line_number =0;

	
	public Component(String [] arguments, String linear_equation){
		number_of_inputs = arguments.length;
		this.arguments = cloneArray(arguments);
		this.linear_equation = linear_equation;
		this.parents = new ArrayList <>();
		this.childs = new ArrayList <>();
		this.inputs_indexes = new ArrayList <>();
	}
	/**
	 * Copy Constructor
	 * @param cpy_c , another component.
	 */
	public Component(Component cpy_c){
		this.number_of_inputs = cpy_c.number_of_inputs;
		this.is_input = cpy_c.is_input;
		this.is_output = cpy_c.is_output;
		this.linear_equation = cpy_c.linear_equation;
		this.arguments = cloneArray(cpy_c.arguments);
		this.inputs_indexes= new ArrayList<>(cpy_c.inputs_indexes);
		this.parents = new ArrayList<>(cpy_c.parents);
		this.childs = new ArrayList<>(cpy_c.childs);
		
	}
	
	public int get_number_of_inputs(){
		return this.number_of_inputs;
	}
	
	public void addIndexOfInput(int i){
		this.inputs_indexes.add(i);
	}
	public List<Integer> getIndexsOfInputs(){
		return this.inputs_indexes;
	}
	public String toString(){
		return this.linear_equation;
	}
	
	public boolean is_input(){
		return this.is_input;
	}
	
	public boolean is_output(){
		return this.is_output;
	}
	public void set_as_input(){
		this.is_input = true;
	}
	
	public void set_as_output(){
		this.is_output = true;
	}
	
	public void add_parent(Component c){
		this.parents.add(c);
	}
	
	public void add_child(Component c){
		this.childs.add(c);
	}
	
	public List<Component> getParents(){
		return this.parents;
	}
	
	public List<Component> getChilds(){
		return this.childs;
	}
	
	private String [] cloneArray( String [] arr){
		String [] new_arr = new String [arr.length];
		for (int i=0; i< arr.length ; i++){
			new_arr[i] = arr[i];
		}
		return new_arr;
	}
	public String get_linear_equation(){
		return this.linear_equation;
	}
	
	public int get_line_number(){
		return this.line_number;
	}
	
	public void set_line_number(int line){
		this.line_number = line;
	}
}

