from PIL import Image, UnidentifiedImageError
from colorama import Fore, Back ,Style


MAX_PIXEL_VAlUE = 255 #!set a constant value 
#!consistency matters 
#!A function for converting the rgb tuples into single brightness numbers 
def pixel_average(rval: int, gval: int, bval: int) ->int: 
    bright_val = (rval + gval + bval) / 3
    return round(bright_val)

def lightness(r: int ,g: int ,b: int):
    mx_val = max(r,g,b)
    mn_val = min(r,g,b)
    light = (mx_val + mn_val) / 2
    return round(light)

def luminosity(rr: int ,gg: int ,bb: int ):
    lumin = (0.21* rr + 0.72 * gg + 0.07 * bb)
    return round(lumin)


#!A function for extracting pixel values from the picture itself
def pixel_value_extract(im, brightness: str, invert: bool = False) ->list:
    half = im.reduce(8) #!returns a Image object 
        
    pixel_val_r = list(half.get_flattened_data(band=0)) #!extract individual values , returns a iterator 
    pixel_val_g = list(half.get_flattened_data(band=1)) #!extract individual values , returns a iterator 
    pixel_val_b = list(half.get_flattened_data(band=2)) #!extract indivdual values, returns a iterator 
    

    brightness_values = [] #!store all the computed average values inside a list
        
    for r,g,b in zip(pixel_val_r,pixel_val_g,pixel_val_b):
        if brightness == "average":
            result = pixel_average(r,g,b)
                
        elif brightness == "lightness":
            result = lightness(r,g,b)
        
        elif brightness == "luminosity":
            result = luminosity(r,g,b)
        
            
        if invert == True:
            result = MAX_PIXEL_VAlUE - result #invert
                    
        brightness_values.append(result)
    
    return brightness_values


def cal_pos(val: int, length: int) -> int:
    position = (val/MAX_PIXEL_VAlUE) * (length-1) #?express the val as a fraction of the maximum, multiple by target range
    return round(position)
#!percentage of the way through the range 
#!Normalization , rescaling values so they fit within a standard range
#!Applying that same proportion to the index range of the character string 

#!a function for pixels represented by ASCII character
def image_to_ascii(bvalues):
    ascii_chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    for value in bvalues:
        new_pos = cal_pos(value,len(ascii_chars)) #?calculate the new position 
        chars = ascii_chars[new_pos] #?access the scaled down position of the ascii chars 
        print(Back.BLUE + Fore.WHITE + chars * 3,end="") #!modify and place colors, formatting 
    
    print(Style.RESET_ALL)


#!Reading the picture file and printing the size of the image 
def out():
    #!write image to a filename
    while True:
        try:
            file_path = input("Enter the image path: ")
    
            brightness = input("Enter the brightness level (average, lightness,luminosity): ").strip().lower()
            if brightness not in ["average","lightness","luminosity"]:
                print("Unrecognized brightness level")
                print("average, lightness, luminosity are allowed ones")
                continue  

            inv = input("darker or lighter:").strip().lower()
            if inv not in ["darker","lighter"]:
                print("Unrecognized invert level")
                continue

        #!subprocess.run(["imagesnap",file_path],capture_output=True,text=True,check=True)

            fp = Image.open(file_path)
    
            if inv == "darker":
                all_values = pixel_value_extract(fp,brightness,invert=True)
            elif inv == "lighter":
                all_values = pixel_value_extract(fp,brightness)

            print("Turning an Image into an ASCII art......")
    
            image_to_ascii(all_values)
    
        except FileNotFoundError: #!expected err 
            print("File not found, provide an existing file!",file_path)
    
        except PermissionError:
            print("Image file can't be read")
    
        except UnidentifiedImageError:
            print("The image cannot be opened and identified")

        except KeyboardInterrupt:
            print("Program terminated")
            break 

        except Exception as e: #!when something unexpected happens, extreme unpexted errors  
            print("Unknown or unexpected error:",e)


if __name__ == "__main__":
    out()

#!low level function knows what happens 
#!high level knows what it means
#!single responsibility 

