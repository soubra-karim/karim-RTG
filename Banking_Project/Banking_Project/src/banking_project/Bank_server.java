package banking_project;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import javax.crypto.Cipher;

import java.math.BigInteger;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.security.*;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;
//import java.util.ArrayList; 
import java.util.HashMap;
import java.util.Map;
import java.util.logging.FileHandler;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

class Bank_server {
    static Logger log = Logger.getLogger("banklog");
    static Logger log_encrypt = Logger.getLogger("banklog_encypted");
    static File logfile;
    static File logfile_encrypt;
    
    public static void log_file_encrypt(String encrypted_string) throws IOException{
        log_encrypt.info(encrypted_string);

    }
    
    public static void log_file(String customerID,String Action) throws IOException{
        log.info(customerID+"||"+Action);
        
    }
    
    public static void save_account(String username,String password,float old_balance,float new_balance) throws FileNotFoundException, IOException{
        FileReader file = new FileReader("userdb.txt");
        BufferedReader r2 = new BufferedReader(file);
        String data;

        StringBuffer file_data = new StringBuffer();
        while((data=r2.readLine())!=null){
            file_data.append(data+ System.lineSeparator());
        }
        String file_data2=file_data.toString();
        r2.close();
        
        file.close();

        System.out.println(file_data2);
        file_data2 = file_data2.replace(username+"||"+password+"||"+String.valueOf(old_balance), username+"||"+password+"||"+String.valueOf(new_balance));
        FileWriter file2 = new FileWriter("userdb.txt");
        BufferedWriter w2 = new BufferedWriter(file2);

        w2.append(file_data2);
        w2.flush();
        w2.close();
        file2.close();
    }
    public static float load_account_balance(String username) throws FileNotFoundException, IOException{
          FileReader file = new FileReader("userdb.txt");
          BufferedReader r2 = new BufferedReader(file);
          String data;
          float balance=0;
          while((data=r2.readLine())!=null){
              String[] user_info = data.split("\\|\\|");
              
              if(username.equals(user_info[0])){

                  balance=Float.parseFloat(user_info[2]);
                  break;
              }
          }
          r2.close();
          file.close();
        return balance;
    }
    public static boolean login(String username, String password) throws IOException {
        // return true for successfull login
        // return false for UNsuccesful login
        File login = new File("userdb.txt");
        if(login.exists()){
          FileReader file = new FileReader("userdb.txt");
          BufferedReader r2 = new BufferedReader(file);
          String data;
          boolean user_login=false;
          while((data=r2.readLine())!=null){
              String[] user_info = data.split("\\|\\|");
              
              if(username.equals(user_info[0]) && password.equals(user_info[1])){

                  user_login=true;
                  break;
              }
          }
          r2.close();
          file.close();
          return user_login;
        }else{
            System.out.println("no users exist");
            return false;
        }
    }
    public static boolean Register(String username,String password) throws IOException{
        
        File reg = new File("userdb.txt");
        float balance=0;
        
        if(reg.createNewFile()){
            try (FileWriter writefile = new FileWriter("userdb.txt",true)) {
                BufferedWriter w = new BufferedWriter(writefile);
//                System.out.println("Printing to file");
//                System.out.println(username+"||"+password+"||"+String.valueOf(balance));
                w.write(username+"||"+password+"||"+String.valueOf(balance));
                w.newLine();
                
                w.close();
                writefile.close();
            }
            
            return true;
        }else{
          FileReader file = new FileReader("userdb.txt");
          BufferedReader r2 = new BufferedReader(file);
          String data;
          boolean user_exists=false;
          while((data=r2.readLine())!=null){
              String[] user_info = data.split("\\|\\|");
              
              if(username.equals(user_info[0])){
                  System.out.println("User already exists");
                  user_exists=true;
                  break;
              }
          }
          r2.close();
          file.close();
          if(!user_exists){
                FileWriter writefile = new FileWriter("userdb.txt",true);
                BufferedWriter w = new BufferedWriter(writefile);
                w.write(username+"||"+password+"||"+String.valueOf(balance));
                w.newLine();
                w.close();
                writefile.close();
                
                return true; 
          }else{
              return false;
          } 
        } 
    }
    static final HashMap<String,Socket> sockets_sessions = new HashMap<String,Socket>();
    
    public static void add_to_hash(String label,Socket sock){
        sockets_sessions.put(label, sock);
    }
       
    public static void main(String[] args) throws IOException, NoSuchAlgorithmException {
        logfile = new File("banklog.log");
        logfile_encrypt = new File("banklog_encrypt.log");
        if(logfile.createNewFile()){
            System.out.println("Generating logfile");
        }else{
            System.out.println("Logfile already generated");
        }
        if(logfile_encrypt.createNewFile()){
            System.out.println("Generating logfile");
        }else{
            System.out.println("Logfile already generated");
        }
        FileHandler handle_log = new FileHandler("banklog.log");
        FileHandler handle_log_encrypt = new FileHandler("banklog_encrypt.log");
        log.addHandler(handle_log);
        log_encrypt.addHandler(handle_log_encrypt);
        SimpleFormatter formatter = new SimpleFormatter();
        SimpleFormatter formatter_e = new SimpleFormatter();
        handle_log.setFormatter(formatter);
        handle_log_encrypt.setFormatter(formatter_e);
        //GENERATE PUBLIC and PRIVATE KEY FOR Bank
        KeyPairGenerator KeyGenKDC = KeyPairGenerator.getInstance("RSA");
        KeyGenKDC.initialize(2048);
        KeyPair pairKDC = KeyGenKDC.generateKeyPair();
        PrivateKey privateKeyKDC = pairKDC.getPrivate();
        PublicKey publicKeyKDC = pairKDC.getPublic();
        
        ServerSocket serverSocket = new ServerSocket(6789); // Example port number
        File publicKeyFileKDC = new File("publicBank.key");
        File privateKeyFileKDC = new File("privateBank.key");
        
        X509EncodedKeySpec x509EncodedKeySpec_priv = new X509EncodedKeySpec(privateKeyKDC.getEncoded()); //saving private key
        X509EncodedKeySpec x509EncodedKeySpec = new X509EncodedKeySpec(publicKeyKDC.getEncoded());
        Files.write(privateKeyFileKDC.toPath(), x509EncodedKeySpec_priv.getEncoded());
        Files.write(publicKeyFileKDC.toPath(), x509EncodedKeySpec.getEncoded());
        
        System.out.println("Server started. Waiting for clients...");

        while (true) {
            Socket clientSocket = serverSocket.accept();            
            System.out.println("Client connected.");
            new Bank_serverthread(clientSocket).start();
        }
    }
}
