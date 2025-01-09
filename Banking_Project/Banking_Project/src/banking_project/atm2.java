package banking_project;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.security.InvalidKeyException;
import java.security.KeyFactory;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;
import java.util.Random;
import java.util.Scanner;
import javax.crypto.Cipher;
import javax.crypto.Mac;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
public class atm2 {
    private PublicKey publicKeyBank;
    private DataInputStream recv;
    private DataOutputStream send;
    private PrivateKey privatekeyATM2;
    private PublicKey publicKeyATM2;
    public SecretKey master_secret_key;
    public SecretKey master_secret_key_mac;
    public String id = "atm2";
    public Socket clientSocket;
    public atm2() throws IOException, NoSuchAlgorithmException, InvalidKeySpecException{
        KeyPairGenerator keyGenA = KeyPairGenerator.getInstance("RSA");
        keyGenA.initialize(2048);
        KeyPair pairATM1 = keyGenA.generateKeyPair();
        privatekeyATM2 = pairATM1.getPrivate();
        publicKeyATM2 = pairATM1.getPublic();
        
        // Save public key A to a file
        File publicKeyFileATM1 = new File("publicATM2.key");
        X509EncodedKeySpec x509EncodedKeySpec = new X509EncodedKeySpec(publicKeyATM2.getEncoded());
        Files.write(publicKeyFileATM1.toPath(), x509EncodedKeySpec.getEncoded());

        

        
    }
    public void close() throws IOException {
        recv.close();
        send.close();
        clientSocket.close();
    }
    public void connect() throws IOException{
        clientSocket = new Socket("localhost", 6789);
        System.out.println("Connected to server.");
        recv = new DataInputStream(clientSocket.getInputStream());
        send = new DataOutputStream(clientSocket.getOutputStream());
    }
    public void get_keys() throws IOException, NoSuchAlgorithmException, InvalidKeySpecException{


        // Import the public B key
        File publicKeyFileBank = new File("publicBank.key");
        byte[] bytes = Files.readAllBytes(publicKeyFileBank.toPath());
        X509EncodedKeySpec spec = new X509EncodedKeySpec(bytes);
        KeyFactory keyFactory = KeyFactory.getInstance("RSA");
        publicKeyBank = keyFactory.generatePublic(spec);
    }
    public void gen_keys_authenticate() throws IOException, Exception{

        
        // Recieve E(PUB, [NK1 || IDK])
        String message1 = recv.readUTF();
        String[] messageParts = message1.split("\\|\\|");
        String message1part1 = messageParts[0];
        String message1part2 = messageParts[1];
        message1part1 = decryptpriv(message1part1, privatekeyATM2);
        message1part2 = decryptpriv(message1part2, privatekeyATM2);
        System.out.println("Recieved message 1(decrypted): " + message1part1 + "||" + message1part2);

        // Send E(PUK, [NB || NK2]) to KDC
        String Na_1 = generateNonce();
        System.out.println("Sending message 2: " + Na_1 + "||" + message1part1);
        String message2part1 = encryptpublickey(Na_1, publicKeyBank);
        String message2part2 = encryptpublickey(message1part1, publicKeyBank);
        String message2 = message2part1 + "||" + message2part2;
        send.writeUTF(message2);
        System.out.println("Sent message 2: " + message2);
        
        // Recieve E(PUB, NK2)
        String message3 = recv.readUTF();
        message3 = decryptpriv(message3, privatekeyATM2);
        System.out.println("Recieved message 3(decrypted): " + message3);

        // Recieve E(PUB, E(PRK, KB))
        String message4 = recv.readUTF();
        System.out.println("Recieved message master secret key encrypted: " + message4);
        String[] message4Parts = message4.split("\\|\\|");
        String message4part1 = message4Parts[0];
        String message4part2 = message4Parts[1];
        message4part1 = decryptpriv(message4part1, privatekeyATM2);
        message4part2 = decryptpriv(message4part2, privatekeyATM2);
        String message4final = message4part1+message4part2;
        message4final = decryptpub(message4final, publicKeyBank);
        System.out.println("Decrypted message master secret key: " + message4final);
        byte[] decodedKey = Base64.getDecoder().decode(message4final);
        master_secret_key = new SecretKeySpec(decodedKey, 0, decodedKey.length, "DES");
        System.out.println("Recieved master seceret key: " + master_secret_key);
        
        String message4_mac = recv.readUTF();
        System.out.println("Recieved message MAC master secret key encrypted: " + message4_mac);
        String[] message4Parts_mac = message4_mac.split("\\|\\|");
        String message4part1_mac = message4Parts_mac[0];
        String message4part2_mac = message4Parts_mac[1];
        message4part1_mac = decryptpriv(message4part1_mac, privatekeyATM2);
        message4part2_mac = decryptpriv(message4part2_mac, privatekeyATM2);
        String message4final_mac = message4part1_mac+message4part2_mac;
        message4final_mac = decryptpub(message4final_mac, publicKeyBank);
        System.out.println("Decrypted message MAC master secret key: " + message4final_mac);
        byte[] decodedKey_mac = Base64.getDecoder().decode(message4final_mac);
        master_secret_key_mac = new SecretKeySpec(decodedKey_mac, 0, decodedKey_mac.length, "DES");
        System.out.println("Recieved message MAC master secret key: " + master_secret_key_mac);
        
    }
    public String generateNonce() {
            Random rand_num = new Random();
            return "" + rand_num.nextInt(100);
    }
    
    public String mac(String plainText) throws NoSuchAlgorithmException, InvalidKeyException{
        Mac signer = Mac.getInstance("HmacSHA256");
        signer.init(master_secret_key_mac);
        byte[] signed_msg=signer.doFinal(plainText.getBytes());
        return new String(signed_msg, StandardCharsets.UTF_8);
    }
    public  String encryptpublickey(String plainText, PublicKey publicKey) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.ENCRYPT_MODE, publicKey);
        byte[] secretMessageBytes = plainText.getBytes(StandardCharsets.UTF_8);
        byte[] encryptedMessageBytes = cipher.doFinal(secretMessageBytes);
        return Base64.getEncoder().encodeToString(encryptedMessageBytes);
    }

    public String encryptpriv(String plainText, PrivateKey privateKey) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.ENCRYPT_MODE, privateKey);
        byte[] secretMessageBytes = plainText.getBytes(StandardCharsets.UTF_8);
        byte[] encryptedMessageBytes = cipher.doFinal(secretMessageBytes);
        return Base64.getEncoder().encodeToString(encryptedMessageBytes);
    }

    public String decryptpriv(String encryptedText, PrivateKey privateKey) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.DECRYPT_MODE, privateKey);
        byte[] decodedMessage = Base64.getDecoder().decode(encryptedText);
        byte[] decryptedBytes = cipher.doFinal(decodedMessage);
        return new String(decryptedBytes, StandardCharsets.UTF_8);
    }
    
    public String decryptpub(String encryptedText, PublicKey publickey) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.DECRYPT_MODE, publickey);
        byte[] decodedMessage = Base64.getDecoder().decode(encryptedText);
        byte[] decryptedBytes = cipher.doFinal(decodedMessage);
        return new String(decryptedBytes, StandardCharsets.UTF_8);
    }
    
    public String encryptDES(String plainText) throws Exception {
        Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, master_secret_key);
        byte[] encryptedBytes = cipher.doFinal(plainText.getBytes());
        return Base64.getEncoder().encodeToString(encryptedBytes);
    }

    public String decryptDES(String encryptedText) throws Exception {
        Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
        cipher.init(Cipher.DECRYPT_MODE, master_secret_key);
        byte[] decryptedBytes = cipher.doFinal(Base64.getDecoder().decode(encryptedText));
        return new String(decryptedBytes);
    }

    public void send_msg (String msg) throws IOException{
        send.writeUTF(msg);
    }
    public String recv_msg() throws IOException{
        return recv.readUTF();
    }
    public String get_id(){
        return id;
    }

    public static void main(String[] args) throws IOException, NoSuchAlgorithmException, InvalidKeySpecException, Exception {
        // may need to move this to a constructor
        
        //generates kers for ATM1
        atm2 atm1 = new atm2();
        
        Scanner scanner = new Scanner(System.in);

        boolean called_flag=false;
        atm1.connect();
        while(true){
            System.out.println("Type 1: register");
            System.out.println("Type 2: login");
            System.out.println("Type 3: check balance");
            System.out.println("Type 4: deposit");
            System.out.println("Type 5: withdraw");
            System.out.println("Type 6: quit");
            String input = scanner.nextLine();
            
            if("1".equals(input)){
                String cmd = "register";
                System.out.println("enter username");
                String username = scanner.nextLine();
                System.out.println("enter password");
                String password = scanner.nextLine();
                // Action||id||username||password
                String id = atm1.get_id();
                atm1.send_msg(cmd+"||"+id+"||"+username+"||"+password);
                String recv_register= atm1.recv_msg();
                if(recv_register.equals("Fail")){
                    System.out.println("Error user not registered");
                    atm1.close();
                    atm1.connect();
                }else{
                    System.out.println("register success");
                    atm1.get_keys();
                    atm1.gen_keys_authenticate();
                    called_flag=true;
                }
            }else if("2".equals(input)){
                String cmd = "login";
                System.out.println("enter username");
                String username = scanner.nextLine();
                System.out.println("enter password");
                String password = scanner.nextLine();
                String id = atm1.get_id();
                atm1.send_msg(cmd+"||"+id+"||"+username+"||"+password);
                String recv_login= atm1.recv_msg();
                if(recv_login.equals("Fail")){
                    System.out.println("Error user not logged in");
                    atm1.close();
                    atm1.connect();
                }else{
                    System.out.println("login success");
                    if(!called_flag){
                        atm1.get_keys();
                        atm1.gen_keys_authenticate();
                    }
                }
            }else if("3".equals(input)){
              
                //check balance : nonce||action||signature
                String cmd = "c";
                String nonce = atm1.generateNonce();
                String msg = nonce + "||" + cmd;
                System.out.println("Sending message");
                System.out.println(msg);
                String sig = atm1.mac(msg);
                String encrypt_msg = atm1.encryptDES(msg);
                String msg_final = encrypt_msg + "||" + sig;
                System.out.println("Encrypted message and signature");
                System.out.println(msg_final);
                atm1.send_msg(msg_final);
             
                // E(Nonce||balance)||signature
                String balance_encrypted = atm1.recv_msg();

                
                String[] balance_parts = balance_encrypted.split("\\|\\|");
                String balance_decrypted = atm1.decryptDES(balance_parts[0]);
                String mac_new = atm1.mac(balance_decrypted);
                System.out.println("Received message encrypted");
                System.out.println(balance_encrypted);
                System.out.println("Received message decrypted");
                System.out.println(balance_decrypted);
                if(balance_parts[1].equals(mac_new)){
                    String[] balance_final = balance_decrypted.split("\\|\\|");
                    System.out.println("Nonce is " + balance_final[0]);
                    System.out.println("Your balance is "+balance_final[1]);
                    
                }else{
                    System.out.println("ERROR message corrupted");
                }
                
            }else if("4".equals(input)){
                //deposit
                try{
                String cmd = "d";
                String nonce = atm1.generateNonce();
                System.out.println("How much would you like to deposit");
                String amount = scanner.nextLine();
                float amt = Float.parseFloat(amount);
                //deposit : E(nonce||action||amount)||signature
                String msg = nonce+"||"+cmd+"||"+amount;
                String sig = atm1.mac(msg);
                System.out.println("Message");
                System.out.println(msg);
                String encrypt_msg = atm1.encryptDES(msg);
                System.out.println("Encrypted message");
                System.out.println(encrypt_msg);
                atm1.send_msg(encrypt_msg+"||"+sig);
                }catch(Exception e){
                    System.out.println("Please enter a number");
                }
                //reply
                
                // E(Nonce||balance)||signature 
                String balance_encrypted = atm1.recv_msg();

                
                String[] balance_parts = balance_encrypted.split("\\|\\|");
                String balance_decrypted = atm1.decryptDES(balance_parts[0]);
                String mac_new = atm1.mac(balance_decrypted);
                System.out.println("Received message");
                System.out.println(balance_encrypted);
                System.out.println("Received message decrypted");
                System.out.println(balance_decrypted);
                if(balance_parts[1].equals(mac_new)){
                    String[] balance_final = balance_decrypted.split("\\|\\|");
                    System.out.println("Nonce is " + balance_final[0]);
                    System.out.println("Your balance is "+balance_final[1]);
                    
                }else{
                    System.out.println("ERROR message corrupted");
                }
            }else if("5".equals(input)){
                //withdraw : E(nonce||action||amount)||signature
                try{
                    String cmd = "w";
                    String nonce = atm1.generateNonce();
                    System.out.println("How much would you like to withdraw");
                    String amount = scanner.nextLine();
                    float amt = Float.parseFloat(amount);
                    //deposit : E(nonce||action||amount)||signature
                    String msg = nonce+"||"+cmd+"||"+amount;
                    System.out.println("Message");
                    System.out.println(msg);
                    
                    String sig = atm1.mac(msg);
                    String encrypt_msg = atm1.encryptDES(msg);
                    System.out.println("Encrypted message");
                    System.out.println(encrypt_msg);
                    atm1.send_msg(encrypt_msg+"||"+sig);
                }catch(Exception e){
                    System.out.println("Please enter a number");
                }
                //reply
                
                // E(Nonce||balance)||signature
                //or
                //E(Nonce||Error||balance)||signature
                String balance_encrypted = atm1.recv_msg();

                
                String[] balance_parts = balance_encrypted.split("\\|\\|");
                String balance_decrypted = atm1.decryptDES(balance_parts[0]);
                String mac_new = atm1.mac(balance_decrypted);
                System.out.println("Received message");
                System.out.println(balance_encrypted);
                System.out.println("Received message decrypted");
                System.out.println(balance_decrypted);
                if(balance_parts[1].equals(mac_new)){
                    String[] balance_final = balance_decrypted.split("\\|\\|");
                    if("L".equals(balance_final[1])){
                        System.out.println("Error");
                        System.out.println("amount chosen is larger than balance");
                        System.out.println("Your balance is " + balance_final[2]);
                    }else{
                        System.out.println("Nonce is " + balance_final[0]);
                        System.out.println("Your balance is "+balance_final[1]);
                    }
                }else{
                    System.out.println("ERROR message corrupted");
                }
            }else if("6".equals(input)){
                atm1.send_msg("q");
                atm1.close();
                return;
            }
                    
        }

    }
}
