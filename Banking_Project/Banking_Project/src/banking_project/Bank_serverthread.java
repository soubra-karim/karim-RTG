package banking_project;

import java.net.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.InvalidKeyException;
import java.security.KeyFactory;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;
import java.util.Random;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.crypto.Cipher;
import javax.crypto.Mac;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

class Bank_serverthread extends Thread {
    private static PrivateKey privatekeyBank;
    private static PublicKey publickeyBank;
    private static PublicKey publicKeyATM1;
    private static PublicKey publicKeyATM2;
    private static PublicKey publicKeyATM3;
    private static final String mastersKeyATM1 = "ABCDEFGH||practice"; 
    private static final String mastersKeyATM2 = "IJKLMNOP||evaluate"; 
    private static final String mastersKeyATM3 = "QRSTUVWX||congress";
//    private static final String symmetricKeyS = "KARIMABC"; 

    private static SecretKey secretKeyATM1;
    private static SecretKey secretKeyATM2;
    private static SecretKey secretKeyATM3;
    private static SecretKey key_to_use;
    private static SecretKey key_to_use_mac;
    private static SecretKey secretKeyATM1_mac;
    private static SecretKey secretKeyATM2_mac;
    private static SecretKey secretKeyATM3_mac;
//    private static SecretKey secretKeyC;
    
    Socket clientSocket = null;

    Bank_serverthread(Socket socket) {
        super("ServerThread");
        this.clientSocket = socket;
    }

    public void run() {
        try{
            //Import all key files
            Path path = Paths.get("privateBank.key");
            byte[] bytes = Files.readAllBytes(path);
            PKCS8EncodedKeySpec spec = new PKCS8EncodedKeySpec(bytes);
            KeyFactory keyFactory = KeyFactory.getInstance("RSA");
            privatekeyBank = keyFactory.generatePrivate(spec);
            
            File publicKeyBank = new File("publicBank.key");
            byte[] bytes2 = Files.readAllBytes(publicKeyBank.toPath());
            X509EncodedKeySpec spec2 = new X509EncodedKeySpec(bytes2);
            KeyFactory keyFactory2 = KeyFactory.getInstance("RSA");
            publickeyBank = keyFactory2.generatePublic(spec2);

            //create DES keys
            String[] mkey_atm1 = mastersKeyATM1.split("\\|\\|");
            String[] mkey_atm2 = mastersKeyATM2.split("\\|\\|");
            String[] mkey_atm3 = mastersKeyATM3.split("\\|\\|");
            
            //generate session keys
            byte[] keyBytesATM1 = mkey_atm1[0].getBytes();
            byte[] keyBytesATM2 = mkey_atm2[0].getBytes();
            byte[] keyBytesATM3 = mkey_atm3[0].getBytes();
            byte[] keyBytesATM1_mac = mkey_atm1[1].getBytes();
            byte[] keyBytesATM2_mac = mkey_atm2[1].getBytes();
            byte[] keyBytesATM3_mac = mkey_atm3[1].getBytes();
            secretKeyATM1 = new SecretKeySpec(keyBytesATM1,"DES");
            secretKeyATM2 = new SecretKeySpec(keyBytesATM2,"DES");
            secretKeyATM3 = new SecretKeySpec(keyBytesATM3,"DES");
            secretKeyATM1_mac = new SecretKeySpec(keyBytesATM1_mac,"DES");
            secretKeyATM2_mac = new SecretKeySpec(keyBytesATM2_mac,"DES");
            secretKeyATM3_mac = new SecretKeySpec(keyBytesATM3_mac,"DES");

//            secretKeyS = new SecretKeySpec(keyBytesAB, "DES");         
        }catch (Exception e){
            System.out.println("error");
        }
        try{
            String id_bank="bank";
            DataInputStream recv = new DataInputStream(clientSocket.getInputStream());
            DataOutputStream send = new DataOutputStream(clientSocket.getOutputStream());
            String m1 = recv.readUTF(); // message Action||id||username||password
            if(m1.equals("q")){
                    Bank_server.log_file("not logged in", "quitting");
                    Bank_server.log_file_encrypt(encryptpublickey("not logged in"+"||"+"quitting",publickeyBank));
                    recv.close();
                    send.close();
                    clientSocket.close();
                    return;
            }
            String[] m1_parts = m1.split("\\|\\|"); 
            String Action = m1_parts[0];
            String id_atm = m1_parts[1];
            String username = m1_parts[2];
            String password = m1_parts[3];
            float old_balance=0;
            
            if("register".equals(Action)){
                boolean success = Bank_server.Register(username,password);
                Bank_server.log_file(username, Action);
                Bank_server.log_file_encrypt(encryptpublickey(username+"||"+Action,publickeyBank));
                if(!success){
                    send.writeUTF("Fail");
                    System.out.println("Fail");
                    recv.close();
                    send.close();
                    clientSocket.close();
                    return;
                }else{
                    old_balance = Bank_server.load_account_balance(username);
                    System.out.println("Success");
                    send.writeUTF("success");
                }
            }else if("login".equals(Action)){
                boolean success = Bank_server.login(username,password);
                Bank_server.log_file(username, Action);
                Bank_server.log_file_encrypt(encryptpublickey(username+"||"+Action,publickeyBank));
                if(!success){
                    send.writeUTF("Fail");
                    System.out.println("Fail");
                    recv.close();
                    send.close();
                    clientSocket.close();
                    return;
                }else{
                    old_balance = Bank_server.load_account_balance(username);
                    System.out.println("Success");
                    send.writeUTF("success");
                    
                } 
            }
            if("atm1".equals(id_atm)){
                    File publicKeyFileatm1 = new File("publicATM1.key");
                    byte[] bytesatm1 = Files.readAllBytes(publicKeyFileatm1.toPath());
                    X509EncodedKeySpec spec_atm1 = new X509EncodedKeySpec(bytesatm1);
                    KeyFactory keyFactory_atm1 = KeyFactory.getInstance("RSA");
                    publicKeyATM1 = keyFactory_atm1.generatePublic(spec_atm1);  
                    String Bnonce = generateNonce();
                    // Send E(PUB, [NK1 || IDK])
                    
                    System.out.println("Sending message 1: " + Bnonce + "||" + id_bank);
                    String message1part1_atm1 = encryptpublickey(Bnonce, publicKeyATM1);
                    String message1part2_atm1 = encryptpublickey(id_bank, publicKeyATM1);
                    String message1_atm1= message1part1_atm1 + "||" + message1part2_atm1;
                    send.writeUTF(message1_atm1);
                    System.out.println("Sent message 1: " + message1_atm1);
                    
                    // Recieve (PUK, [NA || NK1]) 
                    String message2_atm1 = recv.readUTF();
                    String[] messageParts_atm1 = message2_atm1.split("\\|\\|");
                    String message2part1_atm1 = messageParts_atm1[0];
                    String message2part2_atm1 = messageParts_atm1[1];
                    message2part1_atm1 = decryptpriv(message2part1_atm1, privatekeyBank);
                    message2part2_atm1 = decryptpriv(message2part2_atm1, privatekeyBank);
                    System.out.println("Recieved message 2(decrypted): " + message2part1_atm1 + "||" + message2part2_atm1);

                    // Send E(PUB, NK1)
                    System.out.println("Sending message 3: " + message2part2_atm1);
                    String message3_atm1 = encryptpublickey(message2part2_atm1, publicKeyATM1);
                    send.writeUTF(message3_atm1);
                    System.out.println("Sent message 3: " + message3_atm1);
                    
                    // Send E(PUB, E(PRK, KA))
                    String KA_atm1 = Base64.getEncoder().encodeToString(secretKeyATM1.getEncoded());

                    //String KB = "" + secretKeyB;
                    System.out.println("Sending message 4: " + secretKeyATM1);
                    String message4_atm1 = encryptpriv(KA_atm1, privatekeyBank);
                    String firstHalf_atm1 = message4_atm1.substring(0, message4_atm1.length() / 2);
                    String secondHalf_atm1 = message4_atm1.substring(message4_atm1.length() / 2);

                    firstHalf_atm1 = encryptpublickey(firstHalf_atm1, publicKeyATM1);
                    secondHalf_atm1 = encryptpublickey(secondHalf_atm1, publicKeyATM1);
                    String message4Final_atm1 = firstHalf_atm1 + "||" + secondHalf_atm1;

                    send.writeUTF(message4Final_atm1);
                    System.out.println("Sent message 4: " + message4Final_atm1);
                    
                    String KA_atm1_mac = Base64.getEncoder().encodeToString(secretKeyATM1_mac.getEncoded());

                    //String KB = "" + secretKeyB;
                    System.out.println("Sending message 4: " + secretKeyATM1_mac);
                    String message4_atm1_mac = encryptpriv(KA_atm1_mac, privatekeyBank);
                    String firstHalf_atm1_mac = message4_atm1_mac.substring(0, message4_atm1_mac.length() / 2);
                    String secondHalf_atm1_mac = message4_atm1_mac.substring(message4_atm1_mac.length() / 2);

                    firstHalf_atm1_mac = encryptpublickey(firstHalf_atm1_mac, publicKeyATM1);
                    secondHalf_atm1_mac = encryptpublickey(secondHalf_atm1_mac, publicKeyATM1);
                    String message4Final_atm1_mac = firstHalf_atm1_mac + "||" + secondHalf_atm1_mac;

                    send.writeUTF(message4Final_atm1_mac);
                    System.out.println("Sent message 4: " + message4Final_atm1_mac);
                    Bank_server.log_file(id_atm, "Authentication, verification, and key distribution");
                    Bank_server.log_file_encrypt(encryptpublickey(id_atm+"||"+"Authentication, verification, and key distribution",publickeyBank));
                    //load file info
                    
                    key_to_use = secretKeyATM1;
                    key_to_use_mac = secretKeyATM1_mac;

            }else if("atm2".equals(id_atm)){
                    File publicKeyFileatm2 = new File("publicATM2.key");
                    byte[] bytesatm2 = Files.readAllBytes(publicKeyFileatm2.toPath());
                    X509EncodedKeySpec spec_atm2 = new X509EncodedKeySpec(bytesatm2);
                    KeyFactory keyFactory_atm2 = KeyFactory.getInstance("RSA");
                    publicKeyATM2 = keyFactory_atm2.generatePublic(spec_atm2);  
                    String Bnonce = generateNonce();
                    // Send E(PUB, [NK1 || IDK])
                    
                    System.out.println("Sending message 1: " + Bnonce + "||" + id_bank);
                    String message1part1_atm2 = encryptpublickey(Bnonce, publicKeyATM2);
                    String message1part2_atm2 = encryptpublickey(id_bank, publicKeyATM2);
                    String message1_atm2= message1part1_atm2 + "||" + message1part2_atm2;
                    send.writeUTF(message1_atm2);
                    System.out.println("Sent message 1: " + message1_atm2);
                    
                    // Recieve (PUK, [NA || NK1]) 
                    String message2_atm2 = recv.readUTF();
                    String[] messageParts_atm2 = message2_atm2.split("\\|\\|");
                    String message2part1_atm2 = messageParts_atm2[0];
                    String message2part2_atm2 = messageParts_atm2[1];
                    message2part1_atm2 = decryptpriv(message2part1_atm2, privatekeyBank);
                    message2part2_atm2 = decryptpriv(message2part2_atm2, privatekeyBank);
                    System.out.println("Recieved message 2(decrypted): " + message2part1_atm2 + "||" + message2part2_atm2);

                    // Send E(PUB, NK1)
                    System.out.println("Sending message 3: " + message2part2_atm2);
                    String message3_atm2 = encryptpublickey(message2part2_atm2, publicKeyATM2);
                    send.writeUTF(message3_atm2);
                    System.out.println("Sent message 3: " + message3_atm2);
                    
                    // Send E(PUB, E(PRK, KA))
                    String KA_atm2 = Base64.getEncoder().encodeToString(secretKeyATM2.getEncoded());

                    //String KB = "" + secretKeyB;
                    System.out.println("Sending message 4: " + secretKeyATM2);
                    String message4_atm2 = encryptpriv(KA_atm2, privatekeyBank);
                    String firstHalf_atm2 = message4_atm2.substring(0, message4_atm2.length() / 2);
                    String secondHalf_atm2 = message4_atm2.substring(message4_atm2.length() / 2);

                    firstHalf_atm2 = encryptpublickey(firstHalf_atm2, publicKeyATM2);
                    secondHalf_atm2 = encryptpublickey(secondHalf_atm2, publicKeyATM2);
                    String message4Final_atm2 = firstHalf_atm2 + "||" + secondHalf_atm2;

                    send.writeUTF(message4Final_atm2);
                    System.out.println("Sent message 4: " + message4Final_atm2);
                    
                    String KA_atm2_mac = Base64.getEncoder().encodeToString(secretKeyATM2_mac.getEncoded());

                    //String KB = "" + secretKeyB;
                    System.out.println("Sending message 4: " + secretKeyATM2_mac);
                    String message4_atm2_mac = encryptpriv(KA_atm2_mac, privatekeyBank);
                    String firstHalf_atm2_mac = message4_atm2_mac.substring(0, message4_atm2_mac.length() / 2);
                    String secondHalf_atm2_mac = message4_atm2_mac.substring(message4_atm2_mac.length() / 2);

                    firstHalf_atm2_mac = encryptpublickey(firstHalf_atm2_mac, publicKeyATM2);
                    secondHalf_atm2_mac = encryptpublickey(secondHalf_atm2_mac, publicKeyATM2);
                    String message4Final_atm2_mac = firstHalf_atm2_mac + "||" + secondHalf_atm2_mac;

                    send.writeUTF(message4Final_atm2_mac);
                    System.out.println("Sent message 4: " + message4Final_atm2_mac);
                    Bank_server.log_file(id_atm, "Authentication, verificatoin, and key distribution");
                    Bank_server.log_file_encrypt(encryptpublickey(id_atm+"||"+"Authentication, verification, and key distribution",publickeyBank));
                    //load file info
                    
                    key_to_use = secretKeyATM2;
                    key_to_use_mac = secretKeyATM2_mac;
            }else if("atm3".equals(id_atm)){
                    File publicKeyFileatm3 = new File("publicATM3.key");
                    byte[] bytesatm3 = Files.readAllBytes(publicKeyFileatm3.toPath());
                    X509EncodedKeySpec spec_atm3 = new X509EncodedKeySpec(bytesatm3);
                    KeyFactory keyFactory_atm3 = KeyFactory.getInstance("RSA");
                    publicKeyATM3 = keyFactory_atm3.generatePublic(spec_atm3);  
                    String Bnonce = generateNonce();
                    // Send E(PUB, [NK1 || IDK])
                    
                    System.out.println("Sending message 1: " + Bnonce + "||" + id_bank);
                    String message1part1_atm3 = encryptpublickey(Bnonce, publicKeyATM3);
                    String message1part2_atm3 = encryptpublickey(id_bank, publicKeyATM3);
                    String message1_atm3= message1part1_atm3 + "||" + message1part2_atm3;
                    send.writeUTF(message1_atm3);
                    System.out.println("Sent message 1: " + message1_atm3);
                    
                    // Recieve (PUK, [NA || NK1]) 
                    String message2_atm3 = recv.readUTF();
                    String[] messageParts_atm3 = message2_atm3.split("\\|\\|");
                    String message2part1_atm3 = messageParts_atm3[0];
                    String message2part2_atm3 = messageParts_atm3[1];
                    message2part1_atm3 = decryptpriv(message2part1_atm3, privatekeyBank);
                    message2part2_atm3 = decryptpriv(message2part2_atm3, privatekeyBank);
                    System.out.println("Recieved message 2(decrypted): " + message2part1_atm3 + "||" + message2part2_atm3);

                    // Send E(PUB, NK1)
                    System.out.println("Sending message 3: " + message2part2_atm3);
                    String message3_atm3 = encryptpublickey(message2part2_atm3, publicKeyATM3);
                    send.writeUTF(message3_atm3);
                    System.out.println("Sent message 3: " + message3_atm3);
                    
                    // Send E(PUB, E(PRK, KA))
                    String KA_atm3 = Base64.getEncoder().encodeToString(secretKeyATM3.getEncoded());

                    //String KB = "" + secretKeyB;
                    System.out.println("Sending message 4: " + secretKeyATM3);
                    String message4_atm3 = encryptpriv(KA_atm3, privatekeyBank);
                    String firstHalf_atm3 = message4_atm3.substring(0, message4_atm3.length() / 2);
                    String secondHalf_atm3 = message4_atm3.substring(message4_atm3.length() / 2);

                    firstHalf_atm3 = encryptpublickey(firstHalf_atm3, publicKeyATM3);
                    secondHalf_atm3 = encryptpublickey(secondHalf_atm3, publicKeyATM3);
                    String message4Final_atm3 = firstHalf_atm3 + "||" + secondHalf_atm3;

                    send.writeUTF(message4Final_atm3);
                    System.out.println("Sent message 4: " + message4Final_atm3);
                    
                    String KA_atm3_mac = Base64.getEncoder().encodeToString(secretKeyATM3_mac.getEncoded());

                    //String KB = "" + secretKeyB;
                    System.out.println("Sending message 4: " + secretKeyATM3_mac);
                    String message4_atm3_mac = encryptpriv(KA_atm3_mac, privatekeyBank);
                    String firstHalf_atm3_mac = message4_atm3_mac.substring(0, message4_atm3_mac.length() / 2);
                    String secondHalf_atm3_mac = message4_atm3_mac.substring(message4_atm3_mac.length() / 2);

                    firstHalf_atm3_mac = encryptpublickey(firstHalf_atm3_mac, publicKeyATM3);
                    secondHalf_atm3_mac = encryptpublickey(secondHalf_atm3_mac, publicKeyATM3);
                    String message4Final_atm3_mac = firstHalf_atm3_mac + "||" + secondHalf_atm3_mac;

                    send.writeUTF(message4Final_atm3_mac);
                    System.out.println("Sent message 4: " + message4Final_atm3_mac);
                    Bank_server.log_file(id_atm, "Authentication, verificatoin, and key distribution");
                    Bank_server.log_file_encrypt(encryptpublickey(id_atm+"||"+"Authentication, verification, and key distribution",publickeyBank));
                    //load file info
                    
                    key_to_use = secretKeyATM3;
                    key_to_use_mac = secretKeyATM3_mac;  
            }
            
            float new_balance = old_balance;
            while(true){
                //withdraw : E(nonce||action||amount)||signature
                //deposit : E(nonce||action||amount)||signature
                //check balance : E(nonce||action)||signature
                String cmd = recv.readUTF(); 
                if(cmd.equals("q")){
                    Bank_server.log_file(username, "quitting");
                    Bank_server.log_file_encrypt(encryptpublickey(username+"||"+"quitting",publickeyBank));
                    Bank_server.save_account(username, password, old_balance, new_balance);
                    clientSocket.close();
                    break;
                }
                String[] cmd_parts = cmd.split("\\|\\|");
                String cmd_decrypted = decryptDES(cmd_parts[0],key_to_use);
                String[] cmd_parts_nonce_action = cmd_decrypted.split("\\|\\|");
                String action = cmd_parts_nonce_action[1];
                String cmd_mac = mac(cmd_decrypted,id_atm);

                if("c".equals(action) && cmd_mac.equals(cmd_parts[1])){
                    
                    Bank_server.log_file(username, "check balance");
                    Bank_server.log_file_encrypt(encryptpublickey(username+"||"+"check balance",publickeyBank));
                    //reply with
                    // E(nonce||balance)||signature
                    
                    String Nonce = cmd_parts_nonce_action[0];
                    
                    String reply_msg = Nonce+"||"+ String.valueOf(new_balance);
                    String sig = mac(reply_msg,id_atm);
                    String encrypted_msg = encryptDES(reply_msg,key_to_use);
                    send.writeUTF(encrypted_msg+"||"+sig);
                }else if("d".equals(action) && cmd_mac.equals(cmd_parts[1])){
                //reply
                
                // E(Nonce||balance)||signature
                    Bank_server.log_file(username, "deposit");
                    Bank_server.log_file_encrypt(encryptpublickey(username+"||"+"deposit",publickeyBank));
                    new_balance = new_balance + Float.parseFloat(cmd_parts_nonce_action[2]);
                    String Nonce = cmd_parts_nonce_action[0];
                    
                    String reply_msg = Nonce+"||"+ String.valueOf(new_balance);
                    String sig = mac(reply_msg,id_atm);
                    String encrypted_msg = encryptDES(reply_msg,key_to_use);
                    send.writeUTF(encrypted_msg+"||"+sig);
                    
                }else if("w".equals(action) && cmd_mac.equals(cmd_parts[1])){
                    //reply
                
                    // E(Nonce||balance)||signature
                    //or
                    //E(Nonce||Error||balance)||signature
                    Bank_server.log_file(username, "withdraw");
                    Bank_server.log_file_encrypt(encryptpublickey(username+"||"+"withdraw",publickeyBank));
                    float amt = Float.parseFloat(cmd_parts_nonce_action[2]);
                    String Nonce = cmd_parts_nonce_action[0];
                    
                    if(amt > new_balance){
                        Bank_server.log_file(username, "withdraw error");
                        Bank_server.log_file_encrypt(encryptpublickey(username+"||"+"withdraw error",publickeyBank));
                        String Error = "L";
                        String str_balance = String.valueOf(new_balance);
                        String msg = Nonce + "||" + Error + "||" + str_balance;
                        String sig = mac(msg,id_atm);
                        String encrypted_msg = encryptDES(msg,key_to_use);
                        String final_msg = encrypted_msg + "||" + sig;
                        send.writeUTF(final_msg);
                        
                    }else{
                        new_balance = new_balance-amt;
                        String reply_msg = Nonce+"||"+ String.valueOf(new_balance);
                        String sig = mac(reply_msg,id_atm);
                        String encrypted_msg = encryptDES(reply_msg,key_to_use);
                        send.writeUTF(encrypted_msg+"||"+sig);
                    }
                }  
            }
        } catch (IOException ex) {
            Logger.getLogger(Bank_serverthread.class.getName()).log(Level.SEVERE, null, ex);
        } catch (NoSuchAlgorithmException ex) {
            Logger.getLogger(Bank_serverthread.class.getName()).log(Level.SEVERE, null, ex);
        } catch (InvalidKeySpecException ex) {
            Logger.getLogger(Bank_serverthread.class.getName()).log(Level.SEVERE, null, ex);
        } catch (Exception ex) {
            Logger.getLogger(Bank_serverthread.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    private static  String mac(String plainText,String id_atm) throws NoSuchAlgorithmException, InvalidKeyException{
        
        Mac signer = Mac.getInstance("HmacSHA256");
        if("atm1".equals(id_atm)){
            signer.init(secretKeyATM1_mac);
        }else if("atm2".equals(id_atm)){
            signer.init(secretKeyATM2_mac);
        }else if("atm3".equals(id_atm)){
            signer.init(secretKeyATM3_mac);
        }
        byte[] signed_msg=signer.doFinal(plainText.getBytes());
        return new String(signed_msg, StandardCharsets.UTF_8);
    }
    private static String generateNonce() {
            Random rand_num = new Random();
            return "" + rand_num.nextInt(100);
    }
        
   private static String encryptpublickey(String plainText, PublicKey publicKey) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.ENCRYPT_MODE, publicKey);
        byte[] secretMessageBytes = plainText.getBytes(StandardCharsets.UTF_8);
        byte[] encryptedMessageBytes = cipher.doFinal(secretMessageBytes);
        return Base64.getEncoder().encodeToString(encryptedMessageBytes);
    }
    private static String encryptpriv(String plainText, PrivateKey privateKey) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.ENCRYPT_MODE, privateKey);
        byte[] secretMessageBytes = plainText.getBytes(StandardCharsets.UTF_8);
        byte[] encryptedMessageBytes = cipher.doFinal(secretMessageBytes);
        return Base64.getEncoder().encodeToString(encryptedMessageBytes);
    }
    private static String decryptpriv(String encryptedText, PrivateKey privateKey) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.DECRYPT_MODE, privateKey);
        byte[] decodedMessage = Base64.getDecoder().decode(encryptedText);
        byte[] decryptedBytes = cipher.doFinal(decodedMessage);
        return new String(decryptedBytes, StandardCharsets.UTF_8);
    }
    private static String decryptpub(String encryptedText, PublicKey publickey) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.DECRYPT_MODE, publickey);
        byte[] decodedMessage = Base64.getDecoder().decode(encryptedText);
        byte[] decryptedBytes = cipher.doFinal(decodedMessage);
        return new String(decryptedBytes, StandardCharsets.UTF_8);
    }
    private static String encryptDES(String plainText, SecretKey secretkey) throws Exception {
        Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, secretkey);
        byte[] encryptedBytes = cipher.doFinal(plainText.getBytes());
        return Base64.getEncoder().encodeToString(encryptedBytes);
    }
    private static String decryptDES(String encryptedText, SecretKey secretkey) throws Exception {
        Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
        cipher.init(Cipher.DECRYPT_MODE, secretkey);
        byte[] decryptedBytes = cipher.doFinal(Base64.getDecoder().decode(encryptedText));
        return new String(decryptedBytes);
    }
}