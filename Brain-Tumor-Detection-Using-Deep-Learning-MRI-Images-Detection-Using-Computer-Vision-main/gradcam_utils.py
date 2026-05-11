
import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend

def generate_growth_graph(tumor_type, stage, confidence, output_path):
    """
    Generate a simulated tumor growth graph based on stage and type.
    
    Args:
        tumor_type: Type of tumor (pituitary, glioma, meningioma).
        stage: Predicted stage (I, II, III, IV, V).
        confidence: Confidence score.
        output_path: Path to save the graph.
    """
    try:
        # Define growth parameters based on tumor type and stage
        # This is a SIMULATION for visualization purposes
        
        months = np.arange(0, 13, 1) # 0 to 12 months
        
        # Base growth rate (arbitrary units)
        base_rates = {
            'pituitary': 0.05,
            'meningioma': 0.08,
            'glioma': 0.15,
            'notumor': 0.0
        }
        
        # Stage multipliers
        stage_mult = {
            'I': 1.0, 'II': 1.5, 'III': 2.5, 'IV': 4.0, 'V': 6.0, 'N/A': 0.0
        }
        
        rate = base_rates.get(tumor_type, 0.05) * stage_mult.get(stage, 1.0)
        
        # Initial size (arbitrary units)
        initial_size = stage_mult.get(stage, 1.0) * 10
        
        # Untreated growth curve (Exponential-ish)
        untreated_growth = initial_size * np.exp(rate * months)
        
        # Treated growth curve (Decay)
        # Assuming treatment starts at month 0
        treated_growth = initial_size * np.exp(-0.2 * months)
        
        plt.figure(figsize=(10, 6))
        
        # Plot curves
        plt.plot(months, untreated_growth, 'r--', linewidth=2, label='Projected Growth (Untreated)')
        plt.plot(months, treated_growth, 'g-', linewidth=2, label='Projected Reduction (With Treatment)')
        
        # Add markers
        plt.scatter([0], [initial_size], color='black', s=100, zorder=5, label='Current Status')
        
        # Styling
        plt.title(f'Projected Tumor Progression Analysis\nType: {tumor_type.capitalize()} | Stage: {stage}', fontsize=14)
        plt.xlabel('Time (Months)', fontsize=12)
        plt.ylabel('Relative Tumor Size / Severity', fontsize=12)
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.legend()
        
        # Add confidence text
        plt.text(0.5, 0.05, f'Model Confidence: {confidence:.1f}%', 
                 transform=plt.gca().transAxes, ha='center', 
                 bbox=dict(facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()
        
        return True
    except Exception as e:
        print(f"Error generating growth graph: {e}")
        return False

def get_gradcam(model, img_array, class_index, layer_name='block5_conv3'):
    """
    Generate Grad-CAM heatmap for a specific class index.
    
    Args:
        model: The full Keras model.
        img_array: Preprocessed image array (1, 128, 128, 3).
        class_index: The index of the class to visualize.
        layer_name: The name of the convolutional layer in the VGG16 base.
    
    Returns:
        heatmap: The heatmap array.
    """
    try:
        # Find the VGG16 layer
        vgg_layer = None
        for layer in model.layers:
            if 'vgg16' in layer.name.lower():
                vgg_layer = layer
                break
        
        if vgg_layer is None:
            print("VGG16 layer not found")
            return None

        # Create a model that outputs the last conv layer of VGG16 and the VGG16 output
        # We need to access the internal VGG16 model
        last_conv_layer = vgg_layer.get_layer(layer_name)
        vgg_submodel = tf.keras.models.Model(
            inputs=vgg_layer.inputs, 
            outputs=[last_conv_layer.output, vgg_layer.output]
        )

        # Create a model for the classifier part (layers after VGG16)
        classifier_input = tf.keras.Input(shape=vgg_layer.output.shape[1:])
        x = classifier_input
        
        # Find the index of the vgg layer in the main model
        vgg_idx = -1
        for i, layer in enumerate(model.layers):
            if layer == vgg_layer:
                vgg_idx = i
                break
        
        # Reconstruct the classifier part
        for layer in model.layers[vgg_idx+1:]:
            x = layer(x)
        
        classifier_model = tf.keras.models.Model(inputs=classifier_input, outputs=x)

        # Compute gradients
        with tf.GradientTape() as tape:
            # Get conv output and vgg output
            conv_outputs, vgg_output = vgg_submodel(img_array)
            tape.watch(conv_outputs)
            
            # Get final predictions
            preds = classifier_model(vgg_output)
            loss = preds[:, class_index]

        # Get gradients of the loss with respect to the conv outputs
        grads = tape.gradient(loss, conv_outputs)

        # Pool the gradients
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

        # Multiply each channel by "how important this channel is"
        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)

        # Apply ReLU
        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        
        return heatmap.numpy()
        
    except Exception as e:
        print(f"Error in Grad-CAM generation: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_gradcam(img_path, heatmap, output_path_heatmap, output_path_overlay, alpha=0.4):
    """
    Save the heatmap and the superimposed image using OpenCV.
    
    Args:
        img_path: Path to the original image.
        heatmap: The generated heatmap (2D array, 0-1).
        output_path_heatmap: Path to save the raw heatmap.
        output_path_overlay: Path to save the overlay image.
        alpha: Intensity of the heatmap overlay.
    """
    try:
        # Load the original image
        img = cv2.imread(img_path)
        if img is None:
            return False
            
        # Resize heatmap to match image dimensions
        heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
        
        # Rescale heatmap to a range 0-255
        heatmap_uint8 = np.uint8(255 * heatmap)

        # Apply the jet colormap
        # cv2.COLORMAP_JET maps low values to blue, high to red
        jet_heatmap = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)

        # Save the raw heatmap
        cv2.imwrite(output_path_heatmap, jet_heatmap)

        # Superimpose the heatmap on original image
        # Ensure both are same type
        superimposed_img = cv2.addWeighted(jet_heatmap, alpha, img, 1 - alpha, 0)

        # Save the superimposed image
        cv2.imwrite(output_path_overlay, superimposed_img)
        
        return True
    except Exception as e:
        print(f"Error saving Grad-CAM: {e}")
        return False

def visualize_cell_structure(img_path, heatmap, output_path):
    """
    Visualize 'cell division' or cellular structure in the tumor region using Watershed.
    
    Args:
        img_path: Path to the original image.
        heatmap: The generated heatmap (2D array, 0-1).
        output_path: Path to save the visualization.
    """
    try:
        # Load image
        img = cv2.imread(img_path)
        if img is None:
            return False
            
        # Resize heatmap to match image
        heatmap_resized = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
        
        # Create a binary mask from the heatmap (tumor region)
        # Threshold can be adjusted, 0.4 implies moderate to high activation
        _, tumor_mask = cv2.threshold(heatmap_resized, 0.4, 1.0, cv2.THRESH_BINARY)
        tumor_mask = np.uint8(tumor_mask)
        
        # If no tumor region found, return False
        if np.count_nonzero(tumor_mask) == 0:
            return False
            
        # Process the image to find 'cells' within the tumor mask
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Contrast enhancement to make 'cells' more visible
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        gray = clahe.apply(gray)
        
        # Binarize inside the mask
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Noise removal
        kernel = np.ones((3,3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        
        # Sure background area
        sure_bg = cv2.dilate(opening, kernel, iterations=3)
        
        # Finding sure foreground area using distance transform
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        _, sure_fg = cv2.threshold(dist_transform, 0.1 * dist_transform.max(), 255, 0) # Lower threshold for more cells
        
        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)
        
        # Marker labelling
        _, markers = cv2.connectedComponents(sure_fg)
        
        # Add one to all labels so that sure background is not 0, but 1
        markers = markers + 1
        
        # Now, mark the region of unknown with zero
        markers[unknown == 255] = 0
        
        # Apply Watershed
        # We only want to apply this inside the tumor mask to avoid segmenting the whole brain
        # But watershed works on the whole image. We will mask the result later.
        markers = cv2.watershed(img, markers)
        
        # Create a visual overlay
        # Mark boundaries in yellow (0, 255, 255)
        # Only where tumor_mask is active
        
        result_img = img.copy()
        
        # Create a colored mask for boundaries
        boundary_mask = np.zeros_like(img)
        boundary_mask[markers == -1] = [0, 255, 255] # Yellow boundaries
        
        # Apply tumor mask to the boundaries
        # We only want to show boundaries INSIDE the tumor region
        tumor_mask_3ch = cv2.merge([tumor_mask, tumor_mask, tumor_mask])
        boundary_mask = cv2.bitwise_and(boundary_mask, boundary_mask, mask=tumor_mask)
        
        # Overlay boundaries on original image
        # Make boundaries thick and visible
        result_img[boundary_mask > 0] = [0, 255, 255]
        
        # Also add a subtle tint to the cell regions to make them look like "cells"
        # We can use the markers to colorize cells slightly
        
        cv2.imwrite(output_path, result_img)
        return True
        
    except Exception as e:
        print(f"Error in cell visualization: {e}")
        return False
