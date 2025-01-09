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

public class atm {
    private PublicKey publicKeyBank;
    private DataInputStream recv;
    private DataOutputStream send;
    private PrivateKey privatekeyATM1;
    private PublicKey publicKeyATM1;
    public SecretKey master_secret_key;
    public SecretKey master_secret_key_mac;
    public String id = "atm1";
    public Socket clientSocket;
    
    public atm() throws IOException, NoSuchAlgorithmException, InvalidKeySpecException{
        KeyPairGenerator keyGenA = KeyPairGenerator.getInstance("RSA");
        keyGenA.initialize(2048);
        KeyPair pairATM1 = keyGenA.generateKeyPair();
        privatekeyATM1 = pairATM1.getPrivate();
        publicKeyATM1 = pairATM1.getPublic();
        
        // Save public key A to a file
        File publicKeyFileATM1 = new File("publicATM1.key");
        X509EncodedKeySpec x509EncodedKeySpec = new X509EncodedKeySpec(publicKeyATM1.getEncoded());
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
        message1part1 = decryptpriv(message1part1, privatekeyATM1);
        message1part2 = decryptpriv(message1part2, privatekeyATM1);
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
        message3 = decryptpriv(message3, privatekeyATM1);
        System.out.println("Recieved message 3(decrypted): " + message3);

        // Recieve E(PUB, E(PRK, KB))
        String message4 = recv.readUTF();
        System.out.println("Recieved message master secret key encrypted: " + message4);
        String[] message4Parts = message4.split("\\|\\|");
        String message4part1 = message4Parts[0];
        String message4part2 = message4Parts[1];
        message4part1 = decryptpriv(message4part1, privatekeyATM1);
        message4part2 = decryptpriv(message4part2, privatekeyATM1);
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
        message4part1_mac = decryptpriv(message4part1_mac, privatekeyATM1);
        message4part2_mac = decryptpriv(message4part2_mac, privatekeyATM1);
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

    // Register a new user
    public boolean register(String username, String password) throws Exception {
        String cmd = "register";
        // Action||id||username||password
        String id = get_id();
        send_msg(cmd+"||"+id+"||"+username+"||"+password);
        String recv_register= recv_msg();
        if(recv_register.equals("Fail")){
            System.out.println("Error user not registered");
            close();
            connect();
            return false;
        }else{
            System.out.println("register success");
            get_keys();
            gen_keys_authenticate();
            return true;
        }
    }

    // Log in a user
    public boolean login(String username, String password) throws Exception {
        String cmd = "login";
        String id = get_id();
        send_msg(cmd+"||"+id+"||"+username+"||"+password);
        String recv_login= recv_msg();
        if(recv_login.equals("Fail")){
            System.out.println("Error user not logged in");
            close();
            connect();
            return false;
        }else{
            System.out.println("login success");
            get_keys();
            gen_keys_authenticate();
            return true;

            }
        }

    // Check balance
    public String checkBalance() throws Exception {
    //check balance : nonce||action||signature
        String cmd = "c";
        String nonce = generateNonce();
        String msg = nonce + "||" + cmd;
        System.out.println("Sending message");
        System.out.println(msg);
        String sig = mac(msg);
        String encrypt_msg = encryptDES(msg);
        String msg_final = encrypt_msg + "||" + sig;
        System.out.println("Encrypted message and signature");
        System.out.println(msg_final);
        send_msg(msg_final);
             
        // E(Nonce||balance)||signature
        String balance_encrypted = recv_msg();
  
        String[] balance_parts = balance_encrypted.split("\\|\\|");
        String balance_decrypted = decryptDES(balance_parts[0]);
        String mac_new = mac(balance_decrypted);
        System.out.println("Received message encrypted");
        System.out.println(balance_encrypted);
        System.out.println("Received message decrypted");
        System.out.println(balance_decrypted);
        if(balance_parts[1].equals(mac_new)){
            String[] balance_final = balance_decrypted.split("\\|\\|");
            System.out.println("Nonce is " + balance_final[0]);
            System.out.println("Your balance is " + balance_final[1]);  
            return balance_final[1];
        }else{
            System.out.println("ERROR message corrupted");
            return "Error";
        }
    }

    // Deposit amount
    public String deposit(String amount) throws Exception {
        
        String cmd = "d";
        String nonce = generateNonce();
        //deposit : E(nonce||action||amount)||signature
        String msg = nonce+"||"+cmd+"||"+amount;
        String sig = mac(msg);
        System.out.println("Message");
        System.out.println(msg);
        String encrypt_msg = encryptDES(msg);
        System.out.println("Encrypted message");
        System.out.println(encrypt_msg);
        send_msg(encrypt_msg+"||"+sig);
 
        //reply
        //E(Nonce||balance)||signature 
        //E(Nonce||Error||balance)||signature
        String balance_encrypted = recv_msg();
        String[] balance_parts = balance_encrypted.split("\\|\\|");
        String balance_decrypted = decryptDES(balance_parts[0]);
        String mac_new = mac(balance_decrypted);
        System.out.println("Received message");
        System.out.println(balance_encrypted);
        System.out.println("Received message decrypted");
        System.out.println(balance_decrypted);
        if(balance_parts[1].equals(mac_new)){
            String[] balance_final = balance_decrypted.split("\\|\\|");
            System.out.println("Nonce is " + balance_final[0]);
            System.out.println("Your balance is "+ balance_final[1]);
            return balance_final[1];
        }else{
            System.out.println("ERROR message corrupted");
            return "Error";
        }
    }

    // Withdraw amount
    public String withdraw(String amount) throws Exception {
        String cmd = "w";
        String nonce = generateNonce();
        //deposit : E(nonce||action||amount)||signature
        String msg = nonce+"||"+cmd+"||"+amount;
        System.out.println("Message");
        System.out.println(msg);

        String sig = mac(msg);
        String encrypt_msg = encryptDES(msg);
        System.out.println("Encrypted message");
        System.out.println(encrypt_msg);
        send_msg(encrypt_msg+"||"+sig);

        //reply
        // E(Nonce||balance)||signature
        //or
        //E(Nonce||Error||balance)||signature
        String balance_encrypted = recv_msg();
        String[] balance_parts = balance_encrypted.split("\\|\\|");
        String balance_decrypted = decryptDES(balance_parts[0]);
        String mac_new = mac(balance_decrypted);
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
                return "Error";
            }else{
                System.out.println("Nonce is " + balance_final[0]);
                System.out.println("Your balance is "+balance_final[1]);
                return balance_final[1];
            }
        }else{
            System.out.println("ERROR message corrupted");
            return "Error";
        }
    }

    // Close the connection
    public void closeConnection() throws IOException {
        try {
            if (clientSocket != null && !clientSocket.isClosed()) {
                send_msg("q");
                clientSocket.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
