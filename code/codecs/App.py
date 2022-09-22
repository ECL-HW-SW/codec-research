from EVC import EVC
import os


codec = EVC('evc')
# editor = Editor()


out = codec.encode()

# a = codec.parse(f'{file[:-4]}.y4m','fast')

# codec.add_to_csv(f'{file[:-4]}.evc',a)

# a_frames = editor.get_frames(f'RAW_files/{file}',[0,10,20,30,40,50,60])
# b_frames = editor.get_frames(f'decoded_files/{preset}_{file}',[0,10,20,30,40,50,60])

# for i in range(len(a_frames)):
#     a = editor.add_border_and_text(a_frames[i],'Original')
#     b = editor.add_border_and_text(b_frames[i],'Compressed')
#     concatenated_image = editor.concatenate(a,b)
#     editor.save(concatenated_image,f'{file}',f'{file[:-3]}_{i}')