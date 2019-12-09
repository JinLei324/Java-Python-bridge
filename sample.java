
import java.io.*;

class sample{
    public static void main(String args[])
    {
         
        String cwd = System.getProperty("user.dir");
        System.out.println("Current working directory : " + cwd);
        Runtime rt = Runtime.getRuntime();
        String[] commands = {"python3", "calculate_stats.pyc","--path=a01.csv"};
        try{
            Process proc = rt.exec(commands);

            BufferedReader stdInput = new BufferedReader(new 
                InputStreamReader(proc.getInputStream()));

            //BufferedReader stdError = new BufferedReader(new InputStreamReader(proc.getErrorStream()));

            // Read the output from the command
            //System.out.println("Here is the standard output of the command:\n");
            String s = null;
            while ((s = stdInput.readLine()) != null) {
                System.out.println(s);
            }

            //Read any errors from the attempted command
            //System.out.println("Here is the standard error of the command (if any):\n");
            //while ((s = stdError.readLine()) != null) {
            //    System.out.println(s);
            //}
        }catch(IOException e){
            System.out.println("Exception");
        }
    }
}
