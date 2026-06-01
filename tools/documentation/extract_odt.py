import os
import sys
import zipfile
import re
import shutil
from lxml import etree

def extract_odt(odt_file):
    # Get file name without extension
    base_name = os.path.splitext(odt_file)[0]
    
    # Create directory for images
    images_dir = base_name
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    # Open the ODT file (which is a ZIP file)
    with zipfile.ZipFile(odt_file, 'r') as zip_ref:
        # Extract content.xml which contains the document content
        content_xml = zip_ref.read('content.xml')
        
        # Parse XML
        root = etree.fromstring(content_xml)
        
        # Define namespaces
        ns = {
            'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
            'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
            'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
            'draw': 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0',
            'xlink': 'http://www.w3.org/1999/xlink'
        }
        
        # Extract text content for context
        body = root.find('.//office:body', ns)
        text_elements = body.findall('.//text:p', ns)
        
        # Get header context for image naming
        current_header = "document_start"
        for p in text_elements:
            style_name = p.get('{' + ns['text'] + '}style-name', '')
            content = ''.join(p.itertext())
            
            # Check if this is a heading
            if style_name and style_name.startswith('Heading'):
                try:
                    # Update current header for image naming
                    current_header = re.sub(r'[^\w\s]', '', content).replace(' ', '_').lower()
                except:
                    pass
        
        # Extract images
        image_count = 0
        for idx, element in enumerate(zip_ref.namelist()):
            if element.startswith('Pictures/') and not element.endswith('/'):
                # Extract the image
                image_data = zip_ref.read(element)
                image_ext = os.path.splitext(element)[1]
                
                # Create image name with context
                image_name = f"{image_count:03d}_{current_header}{image_ext}"
                image_path = os.path.join(images_dir, image_name)
                
                # Save the image
                with open(image_path, 'wb') as img_file:
                    img_file.write(image_data)
                    
                image_count += 1
        
        print(f"Extracted {image_count} images from {odt_file} to {images_dir}/ directory")

def main():
    # Get all ODT files in current directory
    odt_files = [f for f in os.listdir('.') if f.lower().endswith('.odt')]
    
    if not odt_files:
        print("No ODT files found in the current directory.")
        return
    
    print(f"Found {len(odt_files)} ODT file(s). Processing...")
    
    for odt_file in odt_files:
        try:
            extract_odt(odt_file)
        except Exception as e:
            print(f"Error processing {odt_file}: {str(e)}")
    
    print("Processing complete.")

if __name__ == "__main__":
    main()