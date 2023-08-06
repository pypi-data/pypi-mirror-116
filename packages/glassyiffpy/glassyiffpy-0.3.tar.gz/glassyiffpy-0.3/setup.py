from distutils.core import setup
setup(
  name = 'glassyiffpy',    
  packages = ['glassyiffpy'],   
  version = '0.3',    
  license='MIT',       
  description = 'Simple thingy to interact with yiff-party.com', 
  author = 'Glass-Paramedic',                   
  author_email = 'glass-paramedic@weddit.online',    
  url = 'http://weddit.net',   
  download_url = 'https://github.com/Glass-Paramedic/glassyiffpy/archive/refs/tags/v_03.tar.gz', 
  keywords = ['yiff', 'furry', 'porn'],   
  install_requires=[     
          'requests',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',       
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
