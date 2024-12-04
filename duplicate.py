import os
import imagededup
from imagededup.methods import PHash
from typing import List, Dict

import csv

class ImageDuplicateFinder:
    def __init__(self, image_directory: str):

        self.image_directory = image_directory
        self.phasher = PHash()  
        
    def find_duplicates(self, similarity_threshold: float = 0.90) -> Dict[str, List[str]]:

        # Generate encodings for all images in directory
        encodings = self.phasher.encode_images(image_dir=self.image_directory)
        
        # Find duplicates
        duplicates = self.phasher.find_duplicates(
            encoding_map=encodings, 
            max_distance_threshold=similarity_threshold
        )
        
        # Filter out single-image groups
        filtered_duplicates = {
            img: dupe_list 
            for img, dupe_list in duplicates.items() 
            if dupe_list  
        }
        
        return filtered_duplicates
    
    def print_duplicate_groups(self, duplicates: Dict[str, List[str]]):

        if not duplicates:
            print("No duplicates found.")
            return
        
        print("\n--- Duplicate Images Detected ---")
        for base_image, duplicate_list in duplicates.items():
            print(f"\nBase Image: {base_image}")
            print("Duplicates:")
            for dupe in duplicate_list:
                print(f"  - {dupe}")
    
    def save_duplicate_report(self, 
                               duplicates: Dict[str, List[str]], 
                               output_file: str = 'duplicate_report.csv'):

        # Open the CSV file in write mode
        with open(output_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header row
            writer.writerow(["Base Image", "Duplicate Images"])
            
            # Write duplicate data
            if not duplicates:
                writer.writerow(["No duplicates found", ""])
                return
            
            for base_image, duplicate_list in duplicates.items():
                writer.writerow([base_image, ', '.join(duplicate_list)])
        
        print(f"Duplicate report saved to {output_file}")
    
def main():
    IMAGE_DIRECTORY = 'C:/Users/Asus/Desktop/picsss'  # Directory containing images to check
    
    # Validate directory exists
    if not os.path.exists(IMAGE_DIRECTORY):
        print(f"Error: Directory {IMAGE_DIRECTORY} does not exist.")
        return
    
    # Initialize duplicate finder
    duplicate_finder = ImageDuplicateFinder(IMAGE_DIRECTORY)
    
    try:
        # Find duplicates with 90% similarity threshold
        duplicate_images = duplicate_finder.find_duplicates(similarity_threshold=10)
        
        # Print duplicate groups to console
        duplicate_finder.print_duplicate_groups(duplicate_images)
        
        # Optionally save report to CSV
        duplicate_finder.save_duplicate_report(duplicate_images, output_file='duplicate_report.csv')
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
