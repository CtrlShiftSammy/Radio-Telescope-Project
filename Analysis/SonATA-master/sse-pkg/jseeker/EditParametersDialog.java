/*******************************************************************************

 File:    EditParametersDialog.java
 Project: OpenSonATA
 Authors: The OpenSonATA code is the result of many programmers
          over many years

 Copyright 2011 The SETI Institute

 OpenSonATA is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 OpenSonATA is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with OpenSonATA.  If not, see<http://www.gnu.org/licenses/>.
 
 Implementers of this code are requested to include the caption
 "Licensed through SETI" with a link to setiQuest.org.
 
 For alternate licensing arrangements, please contact
 The SETI Institute at www.seti.org or setiquest.org. 

*******************************************************************************/

package opensonata.dataDisplays;

/*
 * EditParametersDialog.java
 * Created on July 9, 2001, 10:26 AM
 */

/**
 *
 */
public class EditParametersDialog extends javax.swing.JDialog {

    /** Creates new form EditParametersDialog */
    public EditParametersDialog(java.awt.Frame parent, boolean modal,
                                TextUiDialog textUiDialog) {
        super(parent, modal);
        initComponents();
	pdmParameters = new PdmParameters();
	setGuiControlsFromParameters();
        this.textUiDialog = textUiDialog;
    }

    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    private void initComponents() {//GEN-BEGIN:initComponents
        baselinesOnOffButtonGroup = new javax.swing.ButtonGroup();
        buttonGroup2 = new javax.swing.ButtonGroup();
        jTabbedPane1 = new javax.swing.JTabbedPane();
        jPanelPDM = new javax.swing.JPanel();
        jPanelSciDataReq = new javax.swing.JPanel();
        jLabel9 = new javax.swing.JLabel();
        jLabel10 = new javax.swing.JLabel();
        jLabel11 = new javax.swing.JLabel();
        jLabel12 = new javax.swing.JLabel();
        jLabel13 = new javax.swing.JLabel();
        jLabel14 = new javax.swing.JLabel();
        jRadioButtonBaselinesOff = new javax.swing.JRadioButton();
        jRadioButtonBaselinesOn = new javax.swing.JRadioButton();
        jTextField9 = new javax.swing.JTextField();
        jRadioButton4 = new javax.swing.JRadioButton();
        jRadioButton5 = new javax.swing.JRadioButton();
        jRadioButton6 = new javax.swing.JRadioButton();
        jRadioButton7 = new javax.swing.JRadioButton();
        jTextField10 = new javax.swing.JTextField();
        jTextField11 = new javax.swing.JTextField();
        jPanelPdmParamNames = new javax.swing.JPanel();
        jLabelDcLength = new javax.swing.JLabel();
        jLabelPdmSkyFreq = new javax.swing.JLabel();
        jLabelMaxCand = new javax.swing.JLabel();
        jLabel1 = new javax.swing.JLabel();
        jLabel2 = new javax.swing.JLabel();
        jLabel3 = new javax.swing.JLabel();
        jLabel4 = new javax.swing.JLabel();
        jLabel5 = new javax.swing.JLabel();
        jLabel6 = new javax.swing.JLabel();
        jLabel26 = new javax.swing.JLabel();
        jLabel7 = new javax.swing.JLabel();
        jLabel8 = new javax.swing.JLabel();
        jPanelPdmParamValues = new javax.swing.JPanel();
        jTextFieldDCLength = new javax.swing.JTextField();
        jTextFieldPdmSkyFreq = new javax.swing.JTextField();
        jTextFieldMaxCand = new javax.swing.JTextField();
        jTextFieldDaddThresh = new javax.swing.JTextField();
        jTextFieldMainCwThresh = new javax.swing.JTextField();
        jTextFieldRemCwThresh = new javax.swing.JTextField();
        jTextFieldMainOnlyCwThresh = new javax.swing.JTextField();
        jTextFieldPulseThresh = new javax.swing.JTextField();
        jTextFieldTripletThresh = new javax.swing.JTextField();
        jTextFieldSingletThresh = new javax.swing.JTextField();
        jTextFieldBaseSubAve = new javax.swing.JTextField();
        jTextFieldBaseInitAccum = new javax.swing.JTextField();
        jPanelPdmParamUnits = new javax.swing.JPanel();
        jLabel15 = new javax.swing.JLabel();
        jLabel16 = new javax.swing.JLabel();
        jLabel17 = new javax.swing.JLabel();
        jLabel18 = new javax.swing.JLabel();
        jLabel19 = new javax.swing.JLabel();
        jLabel20 = new javax.swing.JLabel();
        jLabel21 = new javax.swing.JLabel();
        jLabel22 = new javax.swing.JLabel();
        jLabel23 = new javax.swing.JLabel();
        jLabel27 = new javax.swing.JLabel();
        jLabel24 = new javax.swing.JLabel();
        jLabel25 = new javax.swing.JLabel();
        jLabel28 = new javax.swing.JLabel();
        jPanelActivity = new javax.swing.JPanel();
        jPanelRFC = new javax.swing.JPanel();
        jPanelIFC = new javax.swing.JPanel();
        jPanel6 = new javax.swing.JPanel();
        jLabelEditParameters = new javax.swing.JLabel();
        jButtonApply = new javax.swing.JButton();
        jButtonCancel = new javax.swing.JButton();
        jButtonRestoreDefaults = new javax.swing.JButton();
        
        
        getContentPane().setLayout(new org.netbeans.lib.awtextra.AbsoluteLayout());
        
        setTitle("jseeker Edit Parameters");
        addWindowListener(new java.awt.event.WindowAdapter() {
            public void windowClosing(java.awt.event.WindowEvent evt) {
                closeDialog(evt);
            }
        });
        
        jTabbedPane1.setName("PDM");
        jPanelPDM.setLayout(new org.netbeans.lib.awtextra.AbsoluteLayout());
        
        jPanelSciDataReq.setLayout(new org.netbeans.lib.awtextra.AbsoluteLayout());
        
        jPanelSciDataReq.setBorder(new javax.swing.border.TitledBorder("Science Data Request"));
        jLabel9.setText("Baselines:");
        jPanelSciDataReq.add(jLabel9, new org.netbeans.lib.awtextra.AbsoluteConstraints(90, 35, -1, -1));
        
        jLabel10.setText("Baseline Reporting rate:");
        jPanelSciDataReq.add(jLabel10, new org.netbeans.lib.awtextra.AbsoluteConstraints(15, 60, -1, -1));
        
        jLabel11.setText("Complex Amplitudes:");
        jPanelSciDataReq.add(jLabel11, new org.netbeans.lib.awtextra.AbsoluteConstraints(30, 95, 130, -1));
        
        jLabel12.setText("Data Request Type:");
        jPanelSciDataReq.add(jLabel12, new org.netbeans.lib.awtextra.AbsoluteConstraints(40, 125, -1, -1));
        
        jLabel13.setText("Frequency:");
        jPanelSciDataReq.add(jLabel13, new org.netbeans.lib.awtextra.AbsoluteConstraints(85, 160, -1, -1));
        
        jLabel14.setText("Subband:");
        jPanelSciDataReq.add(jLabel14, new org.netbeans.lib.awtextra.AbsoluteConstraints(100, 200, -1, -1));
        
        jRadioButtonBaselinesOff.setText("Off");
        baselinesOnOffButtonGroup.add(jRadioButtonBaselinesOff);
        jPanelSciDataReq.add(jRadioButtonBaselinesOff, new org.netbeans.lib.awtextra.AbsoluteConstraints(170, 30, -1, -1));
        
        jRadioButtonBaselinesOn.setSelected(true);
        jRadioButtonBaselinesOn.setText("On");
        baselinesOnOffButtonGroup.add(jRadioButtonBaselinesOn);
        jPanelSciDataReq.add(jRadioButtonBaselinesOn, new org.netbeans.lib.awtextra.AbsoluteConstraints(220, 30, -1, -1));
        
        jTextField9.setText("jTextField9");
        jPanelSciDataReq.add(jTextField9, new org.netbeans.lib.awtextra.AbsoluteConstraints(170, 60, -1, -1));
        
        jRadioButton4.setText("Off");
        jPanelSciDataReq.add(jRadioButton4, new org.netbeans.lib.awtextra.AbsoluteConstraints(170, 90, -1, -1));
        
        jRadioButton5.setText("On");
        jPanelSciDataReq.add(jRadioButton5, new org.netbeans.lib.awtextra.AbsoluteConstraints(220, 90, -1, -1));
        
        jRadioButton6.setText("Freq");
        jPanelSciDataReq.add(jRadioButton6, new org.netbeans.lib.awtextra.AbsoluteConstraints(170, 120, -1, -1));
        
        jRadioButton7.setText("Subband");
        jPanelSciDataReq.add(jRadioButton7, new org.netbeans.lib.awtextra.AbsoluteConstraints(220, 120, -1, -1));
        
        jTextField10.setText("jTextField10");
        jPanelSciDataReq.add(jTextField10, new org.netbeans.lib.awtextra.AbsoluteConstraints(170, 160, -1, -1));
        
        jTextField11.setText("jTextField11");
        jPanelSciDataReq.add(jTextField11, new org.netbeans.lib.awtextra.AbsoluteConstraints(170, 200, -1, -1));
        
        jPanelPDM.add(jPanelSciDataReq, new org.netbeans.lib.awtextra.AbsoluteConstraints(395, 70, 320, 250));
        
        jPanelPdmParamNames.setLayout(new java.awt.GridLayout(0, 1, 0, 8));
        
        jLabelDcLength.setText("Data Collection Length:");
        jLabelDcLength.setHorizontalAlignment(javax.swing.SwingConstants.RIGHT);
        jPanelPdmParamNames.add(jLabelDcLength);
        
        jLabelPdmSkyFreq.setText("PDM Sky Frequency:");
        jLabelPdmSkyFreq.setHorizontalAlignment(javax.swing.SwingConstants.RIGHT);
        jPanelPdmParamNames.add(jLabelPdmSkyFreq);
        
        jLabelMaxCand.setText("Max. number of candidates:");
        jLabelMaxCand.setHorizontalAlignment(javax.swing.SwingConstants.TRAILING);
        jPanelPdmParamNames.add(jLabelMaxCand);
        
        jLabel1.setText("DADD Threshold:");
        jLabel1.setHorizontalAlignment(javax.swing.SwingConstants.TRAILING);
        jPanelPdmParamNames.add(jLabel1);
        
        jLabel2.setText("Main CW Threshold:");
        jLabel2.setHorizontalAlignment(javax.swing.SwingConstants.RIGHT);
        jPanelPdmParamNames.add(jLabel2);
        
        jLabel3.setText("Remote CW Threshold:");
        jLabel3.setHorizontalAlignment(javax.swing.SwingConstants.TRAILING);
        jPanelPdmParamNames.add(jLabel3);
        
        jLabel4.setText("Main Only CW Threshold:");
        jLabel4.setHorizontalAlignment(javax.swing.SwingConstants.TRAILING);
        jPanelPdmParamNames.add(jLabel4);
        
        jLabel5.setText("Pulse Threshold:");
        jLabel5.setHorizontalAlignment(javax.swing.SwingConstants.TRAILING);
        jPanelPdmParamNames.add(jLabel5);
        
        jLabel6.setText("Triplet Threshold:");
        jLabel6.setHorizontalAlignment(javax.swing.SwingConstants.TRAILING);
        jPanelPdmParamNames.add(jLabel6);
        
        jLabel26.setText("Singlet Threshold:");
        jLabel26.setHorizontalAlignment(javax.swing.SwingConstants.TRAILING);
        jPanelPdmParamNames.add(jLabel26);
        
        jLabel7.setText("Baseline Subband Average:");
        jLabel7.setHorizontalAlignment(javax.swing.SwingConstants.TRAILING);
        jPanelPdmParamNames.add(jLabel7);
        
        jLabel8.setText("Baseline Initial Accumulation:");
        jLabel8.setHorizontalAlignment(javax.swing.SwingConstants.TRAILING);
        jPanelPdmParamNames.add(jLabel8);
        
        jPanelPDM.add(jPanelPdmParamNames, new org.netbeans.lib.awtextra.AbsoluteConstraints(5, 15, 185, 350));
        
        jPanelPdmParamValues.setLayout(new java.awt.GridLayout(0, 1, 0, 8));
        
        jTextFieldDCLength.setColumns(3);
        jTextFieldDCLength.setHorizontalAlignment(javax.swing.JTextField.RIGHT);
        jPanelPdmParamValues.add(jTextFieldDCLength);
        
        jTextFieldPdmSkyFreq.setHorizontalAlignment(javax.swing.JTextField.RIGHT);
        jPanelPdmParamValues.add(jTextFieldPdmSkyFreq);
        
        jTextFieldMaxCand.setHorizontalAlignment(javax.swing.JTextField.RIGHT);
        jPanelPdmParamValues.add(jTextFieldMaxCand);
        
        jPanelPdmParamValues.add(jTextFieldDaddThresh);
        
        jPanelPdmParamValues.add(jTextFieldMainCwThresh);
        
        jPanelPdmParamValues.add(jTextFieldRemCwThresh);
        
        jPanelPdmParamValues.add(jTextFieldMainOnlyCwThresh);
        
        jPanelPdmParamValues.add(jTextFieldPulseThresh);
        
        jPanelPdmParamValues.add(jTextFieldTripletThresh);
        
        jPanelPdmParamValues.add(jTextFieldSingletThresh);
        
        jPanelPdmParamValues.add(jTextFieldBaseSubAve);
        
        jPanelPdmParamValues.add(jTextFieldBaseInitAccum);
        
        jPanelPDM.add(jPanelPdmParamValues, new org.netbeans.lib.awtextra.AbsoluteConstraints(200, 15, 80, 350));
        
        jPanelPdmParamUnits.setLayout(new java.awt.GridLayout(0, 1, 0, 8));
        
        jLabel15.setText("Secs");
        jPanelPdmParamUnits.add(jLabel15);
        
        jLabel16.setText("MHz");
        jPanelPdmParamUnits.add(jLabel16);
        
        jLabel17.setText("#");
        jPanelPdmParamUnits.add(jLabel17);
        
        jLabel18.setText("sigma");
        jPanelPdmParamUnits.add(jLabel18);
        
        jLabel19.setText("sigma");
        jPanelPdmParamUnits.add(jLabel19);
        
        jLabel20.setText("sigma");
        jPanelPdmParamUnits.add(jLabel20);
        
        jLabel21.setText("sigma");
        jPanelPdmParamUnits.add(jLabel21);
        
        jLabel22.setText("sigma");
        jPanelPdmParamUnits.add(jLabel22);
        
        jLabel23.setText("sigma");
        jPanelPdmParamUnits.add(jLabel23);
        
        jLabel27.setText("sigma");
        jPanelPdmParamUnits.add(jLabel27);
        
        jLabel24.setText("# subbands");
        jPanelPdmParamUnits.add(jLabel24);
        
        jLabel25.setText("# half frames");
        jPanelPdmParamUnits.add(jLabel25);
        
        jPanelPDM.add(jPanelPdmParamUnits, new org.netbeans.lib.awtextra.AbsoluteConstraints(285, 15, 80, 350));
        
        jLabel28.setText("Note:  This Data Request Section Is Not Yet Operational");
        jPanelPDM.add(jLabel28, new org.netbeans.lib.awtextra.AbsoluteConstraints(400, 30, 350, 40));
        
        jTabbedPane1.addTab("PDM", jPanelPDM);
        
        jPanelActivity.setLayout(new org.netbeans.lib.awtextra.AbsoluteLayout());
        
        jTabbedPane1.addTab("Activity", jPanelActivity);
        
        jTabbedPane1.addTab("RFC", jPanelRFC);
        
        jTabbedPane1.addTab("IFC", jPanelIFC);
        
        jTabbedPane1.addTab("Test Signal", jPanel6);
        
        getContentPane().add(jTabbedPane1, new org.netbeans.lib.awtextra.AbsoluteConstraints(30, 55, 755, 425));
        
        jLabelEditParameters.setText("Edit Parameters:");
        getContentPane().add(jLabelEditParameters, new org.netbeans.lib.awtextra.AbsoluteConstraints(10, 20, 100, 20));
        
        jButtonApply.setText("Apply");
        jButtonApply.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButtonApplyActionPerformed(evt);
            }
        });
        
        getContentPane().add(jButtonApply, new org.netbeans.lib.awtextra.AbsoluteConstraints(625, 490, -1, -1));
        
        jButtonCancel.setText("Cancel");
        jButtonCancel.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButtonCancelActionPerformed(evt);
            }
        });
        
        getContentPane().add(jButtonCancel, new org.netbeans.lib.awtextra.AbsoluteConstraints(705, 490, -1, -1));
        
        jButtonRestoreDefaults.setText("Restore Defaults");
        jButtonRestoreDefaults.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButtonRestoreDefaultsActionPerformed(evt);
            }
        });
        
        getContentPane().add(jButtonRestoreDefaults, new org.netbeans.lib.awtextra.AbsoluteConstraints(485, 490, -1, -1));
        
        pack();
    }//GEN-END:initComponents

    private void jButtonRestoreDefaultsActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButtonRestoreDefaultsActionPerformed
        // Add your handling code here:
        // Restore the default parameters.
        pdmParameters.setDefaults();
        setGuiControlsFromParameters();
        sendParametersToSeeker();
    }//GEN-LAST:event_jButtonRestoreDefaultsActionPerformed

    private void jButtonApplyActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButtonApplyActionPerformed
        // Add your handling code here:

        // Apply Button
        setParametersFromGuiControls();  // apply the changes
        sendParametersToSeeker();
	this.hide();   
    }//GEN-LAST:event_jButtonApplyActionPerformed

     
    private void jButtonCancelActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButtonCancelActionPerformed
        // Add your handling code here:

	setGuiControlsFromParameters();  // restore the previous settings
        this.hide();

    }//GEN-LAST:event_jButtonCancelActionPerformed

    /** Closes the dialog */
    private void closeDialog(java.awt.event.WindowEvent evt) {//GEN-FIRST:event_closeDialog
        setVisible(false);
        dispose();
    }//GEN-LAST:event_closeDialog

    private void sendParametersToSeeker() {
       textUiDialog.sendCommand("pdm set length " + pdmParameters.length);
       //textUiDialog.sendCommand("pdm skyfreq " +  pdmParameters.skyfreq);
       textUiDialog.sendCommand("pdm set maxcand " + pdmParameters.maxcand);
       textUiDialog.sendCommand("pdm set daddthresh " + pdmParameters.daddthresh);
       textUiDialog.sendCommand("pdm set maincwthresh " + pdmParameters.maincwthresh);
       textUiDialog.sendCommand("pdm set remcwthresh "  + pdmParameters.remcwthresh);
       textUiDialog.sendCommand("pdm set mainonlycwthresh " + pdmParameters.mainonlycwthresh);
       textUiDialog.sendCommand("pdm set pulsethresh "  + pdmParameters.pulsethresh);
       textUiDialog.sendCommand("pdm set tripletthresh " + pdmParameters.tripletthresh);
       textUiDialog.sendCommand("pdm set singletthresh " + pdmParameters.singletthresh); 
       textUiDialog.sendCommand("pdm set basesubave " + pdmParameters.basesubave);
       textUiDialog.sendCommand("pdm set baseinitaccum " + pdmParameters.baseinitaccum);

       // ... TBD
    }
    
    /**
    * @param args the command line arguments
    */
    public static void main(String args[]) {
        //new EditParametersDialog(new javax.swing.JFrame(), true).show();
    }

    private class PdmParameters {
        public String length = new String("");
        public String skyfreq = new String("");
        public String maxcand = new String("");
        public String daddthresh = new String("");
        public String maincwthresh = new String("");
        public String remcwthresh = new String("");
        public String mainonlycwthresh = new String("");
        public String pulsethresh = new String("");
        public String tripletthresh = new String("");
        public String singletthresh = new String("");
        public String basesubave = new String("");
        public String baseinitaccum = new String("");

	public PdmParameters() {
	    setDefaults();
	}

	public void setDefaults() {
	    length = "5";
	    skyfreq = "2295.0000";
	    maxcand = "8";
	    daddthresh = "2.000000";
	    maincwthresh = "-20.000000";
	    remcwthresh = "-3.400000";
	    mainonlycwthresh = "-20.000000";
	    pulsethresh = "12";
	    tripletthresh = "48";
	    singletthresh = "100";
	    basesubave = "1";
	    baseinitaccum = "20";

	    // ... TBD
	}
    }

    private void setGuiControlsFromParameters()
    {
	jTextFieldDCLength.setText(pdmParameters.length);
	jTextFieldPdmSkyFreq.setText(pdmParameters.skyfreq);
	jTextFieldMaxCand.setText(pdmParameters.maxcand);
	jTextFieldDaddThresh.setText(pdmParameters.daddthresh);
	jTextFieldMainCwThresh.setText(pdmParameters.maincwthresh);
	jTextFieldRemCwThresh.setText(pdmParameters.remcwthresh);
	jTextFieldMainOnlyCwThresh.setText(pdmParameters.mainonlycwthresh);
	jTextFieldPulseThresh.setText(pdmParameters.pulsethresh);
	jTextFieldTripletThresh.setText(pdmParameters.tripletthresh);
	jTextFieldSingletThresh.setText(pdmParameters.singletthresh);
	jTextFieldBaseSubAve.setText(pdmParameters.basesubave);
	jTextFieldBaseInitAccum.setText(pdmParameters.baseinitaccum);

	// ... TBD
    }
    

    private void setParametersFromGuiControls()
    {
	pdmParameters.length = jTextFieldDCLength.getText();
	pdmParameters.skyfreq = jTextFieldPdmSkyFreq.getText();
	pdmParameters.maxcand = jTextFieldMaxCand.getText();
	pdmParameters.daddthresh = jTextFieldDaddThresh.getText();
	pdmParameters.maincwthresh = jTextFieldMainCwThresh.getText();
	pdmParameters.remcwthresh = jTextFieldRemCwThresh.getText();
	pdmParameters.mainonlycwthresh = jTextFieldMainOnlyCwThresh.getText();
	pdmParameters.pulsethresh = jTextFieldPulseThresh.getText();
	pdmParameters.tripletthresh = jTextFieldTripletThresh.getText();
	pdmParameters.singletthresh = jTextFieldSingletThresh.getText();
	pdmParameters.basesubave = jTextFieldBaseSubAve.getText();
	pdmParameters.baseinitaccum = jTextFieldBaseInitAccum.getText();

	// ... TBD
    }
    
    private TextUiDialog textUiDialog;
    private PdmParameters pdmParameters;

    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.ButtonGroup baselinesOnOffButtonGroup;
    private javax.swing.ButtonGroup buttonGroup2;
    private javax.swing.JTabbedPane jTabbedPane1;
    private javax.swing.JPanel jPanelPDM;
    private javax.swing.JPanel jPanelSciDataReq;
    private javax.swing.JLabel jLabel9;
    private javax.swing.JLabel jLabel10;
    private javax.swing.JLabel jLabel11;
    private javax.swing.JLabel jLabel12;
    private javax.swing.JLabel jLabel13;
    private javax.swing.JLabel jLabel14;
    private javax.swing.JRadioButton jRadioButtonBaselinesOff;
    private javax.swing.JRadioButton jRadioButtonBaselinesOn;
    private javax.swing.JTextField jTextField9;
    private javax.swing.JRadioButton jRadioButton4;
    private javax.swing.JRadioButton jRadioButton5;
    private javax.swing.JRadioButton jRadioButton6;
    private javax.swing.JRadioButton jRadioButton7;
    private javax.swing.JTextField jTextField10;
    private javax.swing.JTextField jTextField11;
    private javax.swing.JPanel jPanelPdmParamNames;
    private javax.swing.JLabel jLabelDcLength;
    private javax.swing.JLabel jLabelPdmSkyFreq;
    private javax.swing.JLabel jLabelMaxCand;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JLabel jLabel4;
    private javax.swing.JLabel jLabel5;
    private javax.swing.JLabel jLabel6;
    private javax.swing.JLabel jLabel26;
    private javax.swing.JLabel jLabel7;
    private javax.swing.JLabel jLabel8;
    private javax.swing.JPanel jPanelPdmParamValues;
    private javax.swing.JTextField jTextFieldDCLength;
    private javax.swing.JTextField jTextFieldPdmSkyFreq;
    private javax.swing.JTextField jTextFieldMaxCand;
    private javax.swing.JTextField jTextFieldDaddThresh;
    private javax.swing.JTextField jTextFieldMainCwThresh;
    private javax.swing.JTextField jTextFieldRemCwThresh;
    private javax.swing.JTextField jTextFieldMainOnlyCwThresh;
    private javax.swing.JTextField jTextFieldPulseThresh;
    private javax.swing.JTextField jTextFieldTripletThresh;
    private javax.swing.JTextField jTextFieldSingletThresh;
    private javax.swing.JTextField jTextFieldBaseSubAve;
    private javax.swing.JTextField jTextFieldBaseInitAccum;
    private javax.swing.JPanel jPanelPdmParamUnits;
    private javax.swing.JLabel jLabel15;
    private javax.swing.JLabel jLabel16;
    private javax.swing.JLabel jLabel17;
    private javax.swing.JLabel jLabel18;
    private javax.swing.JLabel jLabel19;
    private javax.swing.JLabel jLabel20;
    private javax.swing.JLabel jLabel21;
    private javax.swing.JLabel jLabel22;
    private javax.swing.JLabel jLabel23;
    private javax.swing.JLabel jLabel27;
    private javax.swing.JLabel jLabel24;
    private javax.swing.JLabel jLabel25;
    private javax.swing.JLabel jLabel28;
    private javax.swing.JPanel jPanelActivity;
    private javax.swing.JPanel jPanelRFC;
    private javax.swing.JPanel jPanelIFC;
    private javax.swing.JPanel jPanel6;
    private javax.swing.JLabel jLabelEditParameters;
    private javax.swing.JButton jButtonApply;
    private javax.swing.JButton jButtonCancel;
    private javax.swing.JButton jButtonRestoreDefaults;
    // End of variables declaration//GEN-END:variables

}